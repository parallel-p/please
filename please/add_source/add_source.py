import os
import shutil
import logging
from ..package import config
from .. import globalconfig
from ..solution_tester.package_config import PackageConfig
from ..utils.writepackage import writepackage

log = logging.getLogger("please_logger.add_source")

class AddSourceError(Exception):
    pass

def add_main_solution_with_config(package_config, path):
    if not os.getcwd() in os.path.abspath(path):
        raise AddSourceError("Main solution isn't in problem folder!")
    package_config['main_solution'] = os.path.relpath(path)

def add_main_solution (path):
    package_config = PackageConfig.get_config()
    # TODO: check if config is None
    add_main_solution_with_config(package_config, path)
    package_text = package_config.get_text()
    writepackage(package_text)
    log.info("Main solution %s was set successfully", path)
    
def add_solution_with_config (package_config, path, expected_list = [], possible_list = []):
    if not os.path.exists(path):
        raise AddSourceError("There is no such file")
    if not os.getcwd() in os.path.abspath(path):
        raise AddSourceError("Solution isn't in problem folder!")
    config_file = config.Config("")
    config_file["source"] = os.path.relpath(path)
    if expected_list != []:
        config_file ["expected_verdicts"] = expected_list
    if possible_list != []:
        config_file ["possible_verdicts"] = possible_list
    package_config.set("solution", config_file, None, True)

def add_solution (path, expected_list = [], possible_list = []):
    package_config = PackageConfig.get_config()
    # TODO: check if config is None
    add_solution_with_config(package_config, path, expected_list, possible_list)
    package_text = package_config.get_text()
    writepackage(package_text)
    log.info("Solution %s was added successfully", path)
    log.debug("Solution %s with expected: %s and possible: %s was added", path, str(expected_list), str(possible_list))

def add_solution_with_expected(path, expected_list = []):
    add_solution(path, expected_list)

def add_checker_with_config (package_config, path):
    if not os.path.exists(path):
        raise AddSourceError("There is no such file")
    if not os.getcwd() in os.path.abspath(path):
        raise AddSourceError("Checker isn't in problem folder!")
    package_config['checker'] = os.path.relpath(path)

def add_checker (path):
    package_config = PackageConfig.get_config()
    # TODO: check if config is None
    add_checker_with_config(package_config, path)
    package_text = package_config.get_text()
    writepackage(package_text)
    log.info("Checker %s was set successfully", path)
    
def add_validator_with_config (package_config, path):
    if not os.path.exists(path):
        raise AddSourceError("There is no such file")
    if not os.getcwd() in os.path.abspath(path):
        raise AddSourceError("Validator isn't in problem folder!")
    package_config['validator'] = os.path.relpath(path)

def add_validator (path):
    package_config = PackageConfig.get_config()
    # TODO: check if config is None
    add_validator_with_config(package_config, path)
    package_text = package_config.get_text()
    writepackage(package_text)
    log.info("Validator %s was set successfully", path)

