import os
import shutil
import logging
from ..package import config
from .. import globalconfig
from ..solution_tester.package_config import PackageConfig
from .. import svn
from ..utils.writepackage import writepackage

log = logging.getLogger("please_logger.add_source")

#We want svn.ProblemInSvn to be created only once and only if needed
insvn = None

def add_main_solution_with_config(package_config, path):
    global insvn
    if insvn is None:
        insvn = svn.ProblemInSvn()
    temp = os.path.split(path)
    basename = os.path.basename(path)
    path = os.path.join(*temp)
    basename = os.path.basename(path)
    if path.replace("\\", "/") != globalconfig.solutions_dir + "/" + basename:
        dest = os.path.join(globalconfig.solutions_dir, basename) 
        shutil.copy(path, dest)
        insvn.add(dest)
    package_config['main_solution'] = globalconfig.solutions_dir + "/" + basename

def add_main_solution (path):
    global insvn
    if insvn is None:
        insvn = svn.ProblemInSvn()
    package_config = PackageConfig.get_config()
    add_main_solution_with_config(package_config, path)
    package_text = package_config.get_text()
    writepackage(package_text, insvn)   
    log.info("Main solution %s was added successfully", path)
    
def add_solution_with_config (package_config, path, expected_list = [], possible_list = []):
    global insvn
    if insvn is None:
        insvn = svn.ProblemInSvn()
    temp = os.path.split(path)
    basename = os.path.basename(path)
    path = os.path.join(*temp)
    if path.replace("\\", "/") != globalconfig.solutions_dir + "/" + basename:
        dest = os.path.join(globalconfig.solutions_dir, basename) 
        shutil.copy(path, dest)
        insvn.add(dest)
    config_file = config.Config("")
    config_file["source"] = globalconfig.solutions_dir + '/' + basename
    if expected_list != []:
        config_file ["expected_verdicts"] = expected_list
    if possible_list != []:
        config_file ["possible_verdicts"] = possible_list
    package_config.set("solution", config_file, None, True)

def add_solution (path, expected_list = [], possible_list = []):
    global insvn
    if insvn is None:
        insvn = svn.ProblemInSvn()
    package_config = PackageConfig.get_config()
    add_solution_with_config(package_config, path, expected_list, possible_list)
    package_text = package_config.get_text()
    writepackage(package_text, insvn)
    log.info("Solution %s was added successfully", path)
    log.debug("Solution %s with expected: %s and possible: %s was added", path, str(expected_list), str(possible_list))

def add_solution_with_expected(path, expected_list = []):
    add_solution(path, expected_list)

def add_checker_with_config (package_config, path):
    global insvn
    if insvn is None:
        insvn = svn.ProblemInSvn()
    if insvn is None:
        insvn = svn.ProblemInSvn()
    temp = os.path.split(path)
    basename =  os.path.basename(path)
    path = os.path.join(*temp)
    basename =  os.path.basename(path)
    if path.replace("\\", "/") != basename:
        dest = os.path.join(basename) 
        shutil.copy(path, dest)
        insvn.add(dest)
    package_config["checker"] = basename

def add_checker (path):
    global insvn
    if insvn is None:
        insvn = svn.ProblemInSvn()
    if insvn is None:
        insvn = svn.ProblemInSvn()
    package_config = PackageConfig.get_config()
    add_checker_with_config(package_config, path)
    package_text = package_config.get_text()
    writepackage(package_text, insvn)   
    log.info("Checker %s was added successfully", path)
    
def add_validator_with_config (package_config, path):
    global insvn
    if insvn is None:
        insvn = svn.ProblemInSvn()
    if insvn is None:
        insvn = svn.ProblemInSvn()
    basename =  os.path.basename(path)
    if path.replace("\\", "/") != basename:
        dest = os.path.join(basename) 
        shutil.copy(path, dest)
        insvn.add(dest)
    package_config["validator"] = basename

def add_validator (path):
    global insvn
    if insvn is None:
        insvn = svn.ProblemInSvn()
    package_config = PackageConfig.get_config()
    add_validator_with_config(package_config, path)
    package_text = package_config.get_text()
    writepackage(package_text, insvn)  
    log.info("Validator %s was added successfully", path)
