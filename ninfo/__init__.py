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
