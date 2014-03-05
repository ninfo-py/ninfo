import importlib
import logging
logging.basicConfig(level=logging.INFO)

class Wrapper:
    def __init__(self, name):
        self.name=name
    def load(self):
         return importlib.import_module(self.name)
