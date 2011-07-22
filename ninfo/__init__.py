import sys
from pkg_resources import iter_entry_points

class PluginBase(object):

    cachetimeout = 60*60
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
    def __init__(self):
        self.plugin_modules = {}
        for ep in iter_entry_points(group='ninfo.plugin'):
            self.plugin_modules[ep.name] = ep
        self.plugins = {}
        self.plugin_instances = {}

    def get_plugin(self, plugin):
        if plugin in self.plugins:
            return self.plugins[plugin]

        p = self.plugin_modules[plugin].load().plugin_class
        self.plugins[plugin] = p
        return p
    
    def get_inst(self, plugin):
        if plugin in self.plugin_instances:
            return self.plugin_instances[plugin]

        instance = self.get_plugin(plugin)()
        self.plugin_instances[plugin] = instance
        return instance

    def get_info(self, plugin, arg):
        instance = self.get_inst(plugin)
        return instance.get_info(arg)
