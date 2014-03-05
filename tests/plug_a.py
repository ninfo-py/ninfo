from ninfo import PluginBase

class a_plug(PluginBase):
    """a"""
    name    =    'a'
    title   =    'A'
    description   =  'AA'
    cache_timeout   =  60*60
    types   =    ['hostname']
    remote = False

    def setup(self):
        pass

    def get_info(self, arg):
        return "A" * len(arg)

plugin_class = a_plug
