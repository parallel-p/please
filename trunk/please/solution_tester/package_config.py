from ..package.config import Config
import os.path
import io
import logging
from .. import globalconfig
from ..utils.exception import Sorry

class PackageConfigNotFoundException(Sorry):
    pass

#TODO:move it to another directory
class PackageConfig:
    """
    Description:
    PackageConfig is a static package config class that returns Config type from a file *.package.
    PackageConfig checks whether this config has already been returned and doesn't re-parse the
    config file again.

    Usage:
    config = PackageConfig.get_config("default.package", dir=".", package_name="default.package")
    output: instace of a Config class
    example: time_limit = config["time_limit"]
    returns None if config wasn't found
    """

    # We store all configs associated with packages.
    # configs_dict["default_package"] => Config of default package
    # It helps us check whether config has already been parsed.
    configs_dict = {}

    @staticmethod
    def get_config(dir = ".", package_name = globalconfig.default_package, ignore_cache = False):
        package_path = os.path.abspath(os.path.join(dir, package_name))
        if not os.path.exists(package_path):
            return None

        if package_path in PackageConfig.configs_dict and not ignore_cache:
            # This congfig is already registered, return it without extra re-parsing
            return PackageConfig.configs_dict[package_path]
        else:
            # Find full path to the package
            # Parse and register the config
            with open(package_path, encoding = "utf-8") as package_file:
                config_text = package_file.read()
            PackageConfig.configs_dict[package_path] = Config(config_text)
            return PackageConfig.configs_dict[package_path]
