import sys
from pkg_resources import iter_entry_points

class PluginBase(object):
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config
        self.setup()

    def setup(self):
        pass

    def get_info_json(self, arg):
        return self.get_info(arg)

def main():
    arg = sys.argv[1]
    for ep in iter_entry_points(group='ninfo.plugin'):
        plugin = ep.load()
        title = plugin.plugin['title']
        instance = plugin.plugin['class']()

        print title
        print instance.get_info(arg)
