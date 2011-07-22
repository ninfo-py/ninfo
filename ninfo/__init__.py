class PluginBase(object):
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config
        self.setup()
