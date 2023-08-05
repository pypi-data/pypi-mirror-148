import logging
import os
import subprocess
import sys
from pkg_resources import parse_version
import re

from ..exceptions import RunnerError, ConfigException
from ..config import ConfigHolder


class PackageManager:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if PackageManager.__instance is None:
            PackageManager()
        return PackageManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if PackageManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            PackageManager.__instance = self
            self.package_list = self.__get_packages()

    def __get_packages(self):
        packages = {}
        with subprocess.Popen([sys.executable, "-m", "pip", "freeze"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            p.wait()
            installed = list(map(lambda x: x.decode("UTF-8").split("=="), filter(lambda x: b'==' in x, p.stdout.read().splitlines())))
        for name, version in installed:
            packages[name] = parse_version(version)
        logging.debug(f"[PackageManager] Picked up packages: {packages}")
        return packages

    def ensure_more(self, package_list, executable=sys.executable):
        to_install = list(filter(lambda x: not self.__has_package(x), package_list))
        if len(to_install) > 0:
            command = [executable, "-m", "pip", "install"] + to_install
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
                p.wait()
                if p.returncode != 0:
                    sys.stdout.buffer.write(p.stderr.read())
                    raise(RunnerError(f"[PackageManager] Could not install dependencies ({p.returncode})"))
            self.package_list = self.__get_packages()

    # Assumption: there are more hits in the long run, than misses
    def ensure(self, package_string, executable=sys.executable):
        if not self.__has_package(package_string):
            logging.info(f"[PackageManager] Installing {package_string}")
            command = [executable, "-m", "pip", "install", package_string]
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
                p.wait()
                if p.returncode != 0:
                    sys.stdout.buffer.write(p.stderr.read())
                    raise(RunnerError(f"[PackageManager] Could not install dependencies ({p.returncode})"))
            self.package_list = self.__get_packages()
        else:
            logging.info(f"[PackageManager] {package_string} already installed")

    def __has_package(self, package_string):
        package_data = re.split("==|>|>=|<|<=", package_string)
        # check in cache
        if package_data[0] in self.package_list:
            # check if version is needed
            if len(package_data) == 2:
                required_version = parse_version(package_data[1])
                installed_version = self.package_list[package_data[0]]
                comparator = package_string.replace(package_data[0], "").replace(package_data[1], "")
                if comparator == "==":
                    return required_version == installed_version
                elif comparator == ">":
                    return installed_version > required_version
                elif comparator == ">=":
                    return installed_version >= required_version
                elif comparator == "<":
                    return installed_version < required_version
                elif comparator == "<=":
                    return installed_version <= required_version
                else:
                    raise ConfigException(f"Illegal comparator found: {comparator}")
            else:
                return True
        return False


def glob(item, workdir):
    new_command = []
    if "*" in item:
        logging.debug(f"[Globbing] Found item: [{item}]")
        dir = os.path.abspath(os.path.join(workdir, os.path.dirname(item)))
        base_name = os.path.basename(item)
        if os.path.isdir(dir):
            item_parts = base_name.split("*")
            for file in os.listdir(dir):
                # TODO: Fix ordering! A*B = B*A = AB*
                if item_parts[0] in file and item_parts[1] in file:
                    new_item = os.path.join(dir, file)
                    logging.debug(f"[Globbing] Substitute: {new_item}")
                    new_command.append(new_item)
        else:
            raise ConfigException(f"[Globbing] Dir not exists: {dir}")
        return new_command
    else:
        return [item]


def glob_command(command, workdir):
    logging.debug(f"[Globbing] Starting command: {' '.join(command)}")
    new_command = []
    for item in command:
        new_command += glob(item, workdir)
    return new_command


def grab_from(target):
    if "from_env" in target:
        try:
            return os.environ[target["from_env"]]
        except KeyError:
            raise ConfigException(f"Env var unset: {target['from_env']}")
    elif "from_cfg" in target:
        value = ConfigHolder.getInstance().get(target["from_cfg"])
        if len(value) == 0:
            value = None
        return value
    else:
        raise ConfigException(f"Unsupported grabber: {target}")


def gen_dict(list_of_dicts):
    """
    Generates a dictionary from a list of dictionaries composed of
    'name' and 'value' keys.

    [{'name': 'a', 'value': 'b'}] => {'a': 'b'}
    """
    return_dict = {}

    for _dict in list_of_dicts:
        try:
            if isinstance(_dict["value"], str):
                return_dict[_dict["name"]] = _dict["value"]
            else:
                return_dict[_dict["name"]] = grab_from(_dict["value"])
        except KeyError:
            raise ConfigException(f"Invalid dict item: {_dict}")

    return return_dict
