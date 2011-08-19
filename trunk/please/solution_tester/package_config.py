from ..package.config import Config
import os
import io
import logging
from .. import globalconfig

class PackageConfigNotFoundException(Exception):
    pass

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
    """

    # We store all configs associated with packages.
    # configs_dict["default_package"] => Config of default package
    # It helps us check whether config has already been parsed.
    configs_dict = {}

    @staticmethod
    def get_config(dir = ".", package_name = globalconfig.default_package, ignore_cache = False):
        #logger = logging.getLogger("please_logger.check_solution")
        #logging.basicConfig(level=logging.INFO)
        if not os.path.exists(dir):
            #logger.debug("Package dir '" + dir + "' does not exist")
            return False#raise PackageConfigNotFoundException("Package dir '" + dir + "' does not exist")
        if not os.path.exists(os.path.join(dir, package_name)):
            #logger.debug("Package '" + package_name + "' does not exist")
            return False#raise PackageConfigNotFoundException("Package '" + package_name + "' does not exist")

        if package_name in PackageConfig.configs_dict and not ignore_cache:
            # This congfig is already registered, return it without extra re-parsing
            return PackageConfig.configs_dict[package_name]
        else:
            # Find full path to the package
            path_to_package = os.path.join(dir, package_name)
            # Parse and register the config
            f = open(path_to_package, encoding = "utf-8")
            config_text = f.read()
            f.close()
            PackageConfig.configs_dict[package_name] = Config(config_text)
            return PackageConfig.configs_dict[package_name]

    """
    @staticmethod
    def get_config(problem_name, dir = ".", package_name = "default.package"):
        if package_name in PackageConfig.configs_dict:
            # This congfig is already registered, return it without extra re-parsing
            return PackageConfig.configs_dict[package_name]
        else:
            # Find full path to the package
            path_to_package = os.path.join(dir, problem_name, package_name)
            # Parse and register the config
            config_text = io.open(path_to_package).read()
            PackageConfig.configs_dict[package_name] = Config(config_text)
            return PackageConfig.configs_dict[package_name]
    """

