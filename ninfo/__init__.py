from pkg_resources import iter_entry_points

__version__ = "0.9.0"

import memcache

import logging

logger = logging.getLogger("ninfo")

import os

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from mako.template import Template

try:
    from inspect import getargspec
except ImportError:
    from inspect import getfullargspec as getargspec

from inspect import getsourcefile

from ninfo import util
import IPy


def clean_cache_key(s):
    return "".join(c for c in s if 32 < ord(c) < 127).encode("utf-8")


class PluginError(Exception):
    def __init__(self, message, cause):
        super(PluginError, self).__init__(message + ", caused by " + repr(cause))
        self.cause = cause


class PluginInitError(PluginError):
    pass


class PluginBase(object):

    cache_timeout = 60 * 60
    local = True
    remote = True
    template = True
    options = {}
    converters = {}

    def __init__(self, config=None, plugin_config=None):
        self.long_desription = self.__doc__
        if config is None:
            config = {}
        if plugin_config is None:
            plugin_config = {}
        self.config = config
        self.plugin_config = plugin_config
        self.initialized = False
        self._name = self.name
        if "disabled" in plugin_config:
            return

    def init(self):
        if self.initialized:
            return True
        try:
            self.initialized = self.setup() != False
            return self.initialized
        except Exception as e:
            logger.exception("Error initializing plugin %s" % self.name)
            raise PluginInitError("Error initializing plugin %s" % self.name, cause=e)

    def as_json(self):
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "long_description": self.long_description,
            "cache_timeout": self.cache_timeout,
            "types": self.types,
            "local": self.local,
            "remote": self.remote,
        }

    def setup(self):
        return True

    def to_json(self, result):
        return result

    def get_info_json(self, arg):
        return self.to_json(self.get_info(arg))

    def get_info_text(self, arg):
        result = self.get_info(arg)
        return self.render_template("text", arg, result)

    def get_info_html(self, arg):
        result = self.get_info(arg)
        return self.render_template("html", arg, result)

    def _do_render(self, filename, arg, result):
        if filename is None:
            return str(result)
        kw = {}
        if "html" in filename:
            kw["default_filters"] = ["h"]
        t = Template(filename=filename, **kw)
        out = t.render(
            arg=arg,
            plugin=self,
            config=self.config,
            plugin_config=self.plugin_config,
            **result
        )
        return out.lstrip()

    def render_template(self, output_type, arg, result):
        if not result:
            return ""
        filename = self.get_template(output_type)
        if filename is None and output_type == "html":
            filename = self.get_template("text")
            out = self._do_render(filename, arg, result)
            if out:
                out = "<pre>" + out + "</pre>"
            return out

        out = self._do_render(filename, arg, result)
        return out

    def get_template(self, output_type):
        code = getsourcefile(self.__class__)
        path = os.path.dirname(code)
        filename = "%s_template_%s.mako" % (self._name, output_type)
        template = os.path.join(path, filename)
        if os.path.exists(template):
            return template

    def get_converter(self, a, b):
        func = self.converters.get((a, b))
        if func:
            return getattr(self, func)


class Ninfo:
    def __init__(self, config_file=None, plugin_modules=None):
        self.plugin_instances = {}
        if plugin_modules:
            self.plugin_modules = plugin_modules
        else:
            self.plugin_modules = {}
            for ep in iter_entry_points(group="ninfo.plugin"):
                self.plugin_modules[ep.name] = ep

        self.read_config(config_file)

    def __contains__(self, plugin):
        return plugin in self.plugin_modules

    def read_config(self, config_file):
        cp = ConfigParser.ConfigParser()
        if config_file:
            cp.read([config_file])
        elif os.getenv("INFO_CONFIG_FILE"):
            cp.read([os.getenv("INFO_CONFIG_FILE")])
        else:
            cp.read(
                ["/etc/ninfo.conf", os.path.expanduser("~/.ninfo.ini"), "ninfo.ini"]
            )
            # cp.read(["ninfo.ini",os.path.expanduser("~/.ninfo.ini"),"/etc/ninfo.ini"])
        # return a simple nested dictionary structure from the config
        self.config = dict((s, dict(cp.items(s))) for s in cp.sections())

        # Remove disabled plugins
        for section in self.config:
            if "disabled" in self.config[section]:
                plugin_name = section.split(":")[1]
                try:
                    del self.plugin_modules[plugin_name]
                except KeyError:
                    logger.debug(
                        "Plugin %s is disabled in .ini file, but was not found."
                        % plugin_name
                    )
                else:
                    logger.info("Plugin %s disabled via .ini file." % plugin_name)

        # Add entries for a cloned plugin configuration
        for section in self.config:
            clone = self.config[section].get("clone")
            disabled = self.config[section].get("disabled")
            if clone and not disabled and clone in self.plugin_modules:
                plugin_name = section.split(":")[1]
                self.plugin_modules[plugin_name] = self.plugin_modules[clone]

        if "general" not in self.config:
            self.cache = None
            self.local_networks = []
            return

        self.cache_host = self.config["general"].get("memcache_host")
        if self.cache_host:
            self.cache = memcache.Client([self.cache_host])
        else:
            self.cache = None

        networks_str = self.config["general"].get("local_networks", "")
        self.local_networks = [IPy.IP(n) for n in networks_str.split(",")]

    def is_local(self, arg):
        for t in util.get_type(arg):
            if t in ["ip", "ip6"]:
                return util.is_local(self.local_networks, arg)
        return False

    def compatible_argument(self, plugin, arg):
        plug = self.get_plugin(plugin)
        if not plug:
            logger.debug("Skipping plugin %s because plugin does not exist" % plugin)
            return False
        potential_arg_types = util.get_type(arg)
        for arg_type in potential_arg_types:
            if arg_type in plug.types:
                if arg_type in ["ip", "ip6"]:
                    if plug.local == False and self.is_local(arg):
                        logger.debug("Skipping plugin %s because arg is local" % plugin)
                        return False
                    if plug.remote == False and not self.is_local(arg):
                        logger.debug(
                            "Skipping plugin %s because arg is remote" % plugin
                        )
                        return False
                return True
        logger.debug("Skipping plugin %s because arg is the wrong type" % plugin)
        return False

    def get_plugin(self, plugin):
        if plugin not in self.plugin_modules:
            return None
        if plugin in self.plugin_instances:
            return self.plugin_instances[plugin]

        plugin_config_key = "plugin:" + plugin
        plugin_config = self.config.get(plugin_config_key, {})
        if "disabled" in plugin_config:
            return None

        # If this plugin was cloned, merge its config on top of the config from
        # the cloned plugin
        if "clone" in plugin_config:
            clone_key = "plugin:" + plugin_config["clone"]
            new_cfg = self.config.get(clone_key, {}).copy()
            new_cfg.update(plugin_config)
            plugin_config = new_cfg

        try:
            cls = self.plugin_modules[plugin].load().plugin_class
            cls.long_description = cls.__doc__
        except:
            logger.exception("Error loading plugin %s" % plugin)
            if plugin in self.plugin_modules:
                del self.plugin_modules[plugin]
            return

        instance = cls(config=self.config, plugin_config=plugin_config)
        # override any plugin metadata for the case of cloned plugins(or otherwise)
        instance.name = plugin
        for field in "name", "title", "description":
            if field in plugin_config:
                setattr(instance, field, plugin_config[field])
        self.plugin_instances[plugin] = instance
        return instance

    @property
    def plugins(self):
        plugins = [self.get_plugin(p) for p in sorted(self.plugin_modules.keys())]
        return [p for p in plugins if p]

    def get_info(self, plugin, arg, options={}, retries=1):
        """Call `plugin` with `arg`, `options` and cache and return the result"""
        if not self.compatible_argument(plugin, arg):
            return None
        plugin_obj = self.get_plugin(plugin)
        timeout = plugin_obj.cache_timeout
        if self.cache and timeout:
            KEY = "ninfo:%s:%s" % (plugin, arg)
            KEY += ":" + ":".join(
                [
                    "%s=%s" % (key, value)
                    for (key, value) in options.items()
                    if key in plugin_obj.options
                ]
            )
            # Remove non-alphanumerics from key, to be safe
            KEY = clean_cache_key(KEY)
            ret = self.cache.get(KEY)
            if ret:
                return ret[1]

        try:
            plugin_obj.init()
            get_info_args = len(getargspec(plugin_obj.get_info)[0])
            if get_info_args == 3:
                # This plugin supports context.
                ret = plugin_obj.get_info(arg, options)
            else:
                # This plugin doesn't.
                ret = plugin_obj.get_info(arg)
            if self.cache and timeout:
                self.cache.set(KEY, (True, ret), timeout)
            return ret
        except PluginInitError:
            raise
        except Exception as e:
            logger.exception("Error running plugin %s" % plugin)
            if retries:
                return self.get_info(plugin, arg, options, retries - 1)
            raise PluginError("Error running plugin %s" % plugin, cause=e)

    def get_info_json(self, plugin, arg, options={}):
        result = self.get_info(plugin, arg, options)

        p = self.get_plugin(plugin)
        return p.to_json(result)

    def get_info_text(self, plugin, arg, options={}):
        result = self.get_info(plugin, arg, options)

        p = self.get_plugin(plugin)
        return p.render_template("text", arg, result)

    def get_info_html(self, plugin, arg, options={}):
        result = self.get_info(plugin, arg, options)

        p = self.get_plugin(plugin)
        return p.render_template("html", arg, result)

    def get_info_iter(self, arg, plugins=None, options={}):
        for p in sorted(self.plugins, key=lambda p: p.name):
            if plugins and p.name not in plugins:
                continue
            if not self.compatible_argument(p.name, arg):
                continue
            try:
                result = self.get_info(p.name, arg, options)
                yield p, result
            except PluginError:
                logger.exception("Error running plugin %s", p.name)

    def get_info_dict(self, arg):
        res = {}
        for p, result in self.get_info_iter(arg):
            res[p.name] = result
        return res

    def show_info(self, arg, plugins=None, options={}):
        for p, result in self.get_info_iter(arg, plugins, options):
            print("*** %s (%s) ***" % (p.title, p.description))
            print(p.render_template("text", arg, result))

    def convert(self, arg, to_type):
        potential_arg_types = util.get_type(arg)
        for p in self.plugins:
            for arg_type in potential_arg_types:
                try:
                    if (arg_type, to_type) in p.converters:
                        p.init()
                        yield p.name, p.get_converter(arg_type, to_type)(arg)
                except Exception:
                    logger.exception("Error running plugin %s", p.name)


def main():
    logging.basicConfig(level=logging.INFO)
    # requests logs stuff at level INFO
    logging.getLogger("requests.packages.urllib3").setLevel(logging.ERROR)

    from optparse import OptionParser

    parser = OptionParser(usage="usage: %prog [options] [addresses]")
    parser.add_option("-p", "--plugin", dest="plugins", action="append", default=None)
    parser.add_option("-l", "--list", dest="list", action="store_true", default=False)
    (options, complete_args) = parser.parse_args()

    p = Ninfo()
    if options.list:
        print("%-20s %-20s %s" % ("Name", "Title", "Description"))
        for pl in p.plugins:
            print("%-20s %-20s %s" % (pl.name, pl.title, pl.description))
        return

    context_options = {}
    args = []
    for arg in complete_args:
        if "=" in arg:
            (ctxt_name, ctxt_value) = arg.split("=", 1)
            context_options[ctxt_name] = ctxt_value
        else:
            args.append(arg)

    plugins = options.plugins or None
    for arg in args:
        if len(args) != 1:
            print("=== %s === " % (arg,))
        p.show_info(arg, plugins=plugins, options=context_options)


if __name__ == "__main__":
    main()
