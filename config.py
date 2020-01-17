"""
    This code is inspired by http://code.activestate.com/recipes/577887-a-simple-namespace-class/
"""

import os
import json

class ConfigurationManager(dict):
    """
        A dict subclass that exposes its items as attributes.
    """

    def __init__(self, config_fname='app_config.json', **kwargs):
        self.fname = '/sd/%s' % config_fname

        # Load config from file if exists
        if os.path.exists(self.fname):
            with open(self.fname, 'r') as f:
                ftxt = f.read()
            config_dict = json.loads(ftxt)

        super().__init__({**config_dict, **kwargs})

    def _store_dict(self):
        d = {k:self[k] for k in dir(self)}
        with open(self.fname, 'w') as f: 
            f.write(json.dumps(d))

    def __dir__(self):
        return tuple(self)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, super().__repr__())

    def __getattribute__(self, name):
        try:
            return self[name]
        except KeyError:
            msg = "'%s' object has no attribute '%s'"
            raise AttributeError(msg % (type(self).__name__, name))

    def __setattr__(self, name, value):
        self[name] = value
        self._store_dict()

    def __delattr__(self, name):
        del self[name]

    #------------------------
    # static methods

    @staticmethod
    def hasattr(ns, name):
        try:
            object.__getattribute__(ns, name)
        except AttributeError:
            return False
        return True

    @staticmethod
    def getattr(ns, name):
        return object.__getattribute__(ns, name)

    @staticmethod
    def setattr(ns, name, value):
        return object.__setattr__(ns, name, value)

    @staticmethod
    def delattr(ns, name):
        return object.__delattr__(ns, name)

