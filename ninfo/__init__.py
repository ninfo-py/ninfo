import sys
from pkg_resources import iter_entry_points

import memcache

import logging
logger = logging.getLogger("ninfo")

import os
import ConfigParser

from mako.template import Template

class PluginBase(object):

    cache_timeout = 60*60
    local = True

    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config
        self.setup()

    def setup(self):
        pass

    def get_info_json(self, arg):
        return self.get_info(arg)

class Ninfo:
    def __init__(self, config_file=None):
        self.plugins = {}
        for ep in iter_entry_points(group='ninfo.plugin'):
            self.plugins[ep.name] = ep
        self.plugin_modules = {}
        self.plugin_instances = {}

        self.read_config(config_file)
        self.cache_host = self.config['general'].get('memcache_host')
        if self.cache_host:
            self.cache = memcache.Client([self.cache_host])
        else:
            self.cache = None

    def read_config(self, config_file):
        cp = ConfigParser.ConfigParser()
        if config_file:
            cp.read([config_file])
        elif os.getenv("INFO_CONFIG_FILE"):
            cp.read([os.getenv("INFO_CONFIG_FILE")])
        else:
            cp.read(["ninfo.ini","/etc/ninfo.ini"])
        #return a simple nested dictionary structure from the config
        self.config = dict((s, dict(cp.items(s))) for s in cp.sections())

    def get_plugin(self, plugin):
        if plugin in self.plugin_modules:
            return self.plugin_modules[plugin]

        p = self.plugins[plugin].load().plugin_class
        self.plugin_modules[plugin] = p
        return p
    
    def get_inst(self, plugin):
        if plugin in self.plugin_instances:
            return self.plugin_instances[plugin]

        instance = self.get_plugin(plugin)()
        self.plugin_instances[plugin] = instance
        return instance

    def get_info(self, plugin, arg):

        if self.cache:
            KEY = 'ninfo:%s:%s' % (plugin, arg)
            ret = self.cache.get(KEY)
            if ret:
                return ret[1]

        try:
            instance = self.get_inst(plugin)
            ret = instance.get_info(arg)
            if self.cache:
                timeout = self.get_plugin(plugin).cache_timeout
                self.cache.set(KEY, (True, ret), timeout)
            return ret
        except Exception, e:
            logger.exception("Error running plugin %s" % plugin)
            raise
