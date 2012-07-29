import os.path
from .config import ConfigFile, Config
from .. import globalconfig
from ..utils.writepackage import writepackage

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
    def get_config(dir = None, package_name = globalconfig.default_package, ignore_cache = False):
        if dir is None:
            dir = globalconfig.problem_folder
        if dir is None:
            dir = '.'
        package_path = os.path.abspath(os.path.join(dir, package_name))
        if not os.path.exists(package_path):
            return None

        if package_path in PackageConfig.configs_dict and not ignore_cache:
            # This config is already registered, return it without extra re-parsing
            return PackageConfig.configs_dict[package_path]
        else:
            # Find full path to the package
            # Parse and register the config
            PackageConfig.configs_dict[package_path] = pc = ConfigFile(package_path)
            PackageConfig.oldversion_fix(pc)
            return pc

    @staticmethod
    def oldversion_fix(conf):
        '''Fix *.package 
           and rewrite please_version to current
        '''
        if conf['please_version'] != globalconfig.please_version:
            if float(conf['please_version']) < 0.25 and float(globalconfig.please_version) > 0.25:
                PackageConfig.main_solution_fix(conf)

            conf['please_version'] = str(globalconfig.please_version)
            conf.write()


    @staticmethod
    def main_solution_fix(conf):
        '''In please version <0.3 main_solution was not described
           in solutions config. 
        '''
        new_config = Config("")
        new_config["source"] = conf['main_solution']
        new_config["expected"] = ["OK", ]
        conf.set("solution", new_config, None, True)

