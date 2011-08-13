import os
import shutil
import sys
from ..package import config
import logging
from .. import globalconfig
from ..solution_tester.package_config import PackageConfig

log = logging.getLogger("please_logger.add_source")

def __writepackage(text):
    output_stream = open(globalconfig.default_package, "w", encoding = "utf-8")
    output_stream.write(text)
    output_stream.close()

def add_main_solution_with_config(package_config, path):
    temp = os.path.split(path)
    basename = os.path.basename(path)
    path = os.path.join(*temp)
    basename = os.path.basename(path)
    if path.replace("\\", "/") != globalconfig.solutions_dir + "/" + basename:
        shutil.copy(path, os.path.join(globalconfig.solutions_dir, basename))
    package_config['main_solution'] = globalconfig.solutions_dir + "/" + basename

def add_main_solution (path):
    package_config = PackageConfig.get_config()
    add_main_solution_with_config(package_config, path)
    package_text = package_config.get_text()
    __writepackage(package_text)   
    log.info("Main solution %s was added successfully", path)
    
def add_solution_with_config (package_config, path, expected_list = [], possible_list = []):
    temp = os.path.split(path)
    basename = os.path.basename(path)
    path = os.path.join(*temp)
    if path.replace("\\", "/") != globalconfig.solutions_dir + "/" + basename:
        shutil.copy(path, os.path.join(globalconfig.solutions_dir, basename))
    config_file = config.Config("")
    config_file["source"] = globalconfig.solutions_dir + '/' + basename
    if expected_list != []:
        config_file ["expected_verdicts"] = expected_list
    if possible_list != []:
        config_file ["possible_verdicts"] = possible_list
    package_config.set("solution", config_file, None, True)

def add_solution (path, expected_list = [], possible_list = []):
    package_config = PackageConfig.get_config()
    add_solution_with_config(package_config, path, expected_list, possible_list)
    package_text = package_config.get_text()
    __writepackage(package_text)
    log.info("Solution %s was added successfully", path)
    log.debug("Solution %s with expected: %s and possible: %s was added", path, str(expected_list), str(possible_list))

def add_solution_with_expected(path, expected_list = []):
    add_solution(path, expected_list)

def add_checker_with_config (package_config, path):
    temp = os.path.split(path)
    basename =  os.path.basename(path)
    path = os.path.join(*temp)
    basename =  os.path.basename(path)
    if path.replace("\\", "/") != basename:
        shutil.copy(path, os.path.join(basename))
    package_config["checker"] = basename

def add_checker (path):
    package_config = PackageConfig.get_config()
    add_checker_with_config(package_config, path)
    package_text = package_config.get_text()
    __writepackage(package_text)   
    log.info("Checker %s was added successfully", path)
    
def add_validator_with_config (package_config, path):
    basename =  os.path.basename(path)
    if path.replace("\\", "/") != basename:
        shutil.copy(path, os.path.join(basename))
    package_config["validator"] = basename

def add_validator (path):
    package_config = PackageConfig.get_config()
    add_validator_with_config(package_config, path)
    package_text = package_config.get_text()
    __writepackage(package_text)  
    log.info("Validator %s was added successfully", path)
