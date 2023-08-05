import logging
import os

from .exceptions import ConfigException


class ConfigHolder:
    __instance = None
    file_name = os.path.join(os.getcwd(), ".alice", "vars")

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ConfigHolder.__instance is None:
            ConfigHolder()
        return ConfigHolder.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ConfigHolder.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ConfigHolder.__instance = self
            config = os.path.abspath(os.path.join(os.getcwd(), self.file_name))
            self.vars = {}
            if os.path.isfile(config):
                with open(config) as f:
                    for _line in f:
                        line = _line.strip()
                        items = line.split("=")
                        if len(items) > 1:
                            self.vars[items[0]] = line.replace(f"{items[0]}=", "")
            logging.debug(f"Loaded from {self.file_name}: {self.vars}")

    def get(self, key):
        try:
            return self.vars[key]
        except KeyError:
            raise ConfigException(f"{key} not defined in .conf!")

    def set(self, key, value):
        self.vars[key] = value
        self.commit()

    def soft_set(self, key, value):
        self.vars[key] = value

    def commit(self):
        with open(self.file_name, 'w') as f:
            for k, v in self.vars.items():
                f.write(f"{k}={v if v is not None else ''}\n")
