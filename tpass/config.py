import simplejson

from collections import UserDict


class Config(UserDict):
    def __init__(self, config_file):
        self._config_file = config_file
        with open(config_file) as f:
            self.data = simplejson.load(f)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        with open(self._config_file, "w") as f:
            simplejson.dump(self.data, f, indent=4)
