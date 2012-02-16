import os
import logging
from ..package import config
from ..package.package_config import PackageConfig
from ..utils.writepackage import writepackage
from ..utils.exceptions import PleaseException

log = logging.getLogger("please_logger.add_source")

def add_main_solution_with_config(package_config, path):
    if not os.getcwd() in os.path.abspath(path):
        raise PleaseException("Main solution isn't in problem folder!")
    abspath = os.path.abspath(path)
    for num, solve in enumerate(package_config["solution"]):
        if abspath == os.path.abspath(solve["source"]):
            package_config.delete("solution", num)
            log.warning("Main solution must have no config, so we firstly delete this existing config")
            break
    package_config['main_solution'] = os.path.relpath(path)

def add_main_solution (path):
    package_config = PackageConfig.get_config()
    add_main_solution_with_config(package_config, path)
    package_text = package_config.get_text()
    writepackage(package_text)
    log.info("Main solution %s has bee set successfully", path)

def del_solution(path):
    config = PackageConfig.get_config()
    abspath = os.path.abspath(path)
    if config["solution"] is not None:
        for num, solve in enumerate(config["solution"]):
            if os.path.abspath(solve["source"]) == abspath:
                config.delete("solution", num)
                writepackage(config.get_text())
                log.info("Solution config has been deleted")
                return
    raise PleaseException("There is no such solution")
    
def get_dict_from_args(args, changing=False):
    result = {}
    last_item = None
    list_items = ["expected", "possible"]
    simple_items = ["input", "output"]
    assigned = True
    for item in args:
        if item in simple_items or item in list_items:
            if assigned == False:
                raise PleaseException("Keyword '" + last_item + "' has no assignment")
            last_item = item
            assigned = False
        elif last_item is None:
            raise PleaseException("First argument is not a solution keyword")
        else:
            if last_item in list_items:
                result.setdefault(last_item, []).append(item)
            else:
                if assigned:
                    raise PleaseException("Value for keyword '" + last_item + "' is already assigned")
                result[last_item] = item
            assigned = True
    if assigned == False:
        raise PleaseException("Keyword '" + last_item + "' has no assignment")
    return result

def fix_args_user_mistakes(properties):
    for arg in ["expected", "possible"]:
        if arg in properties:
            responces = set([x.upper() for x in properties[arg]])
            for responce in responces:
                if responce not in ["OK", "WA", "RE", "TL", "ML"]:
                    raise PleaseException("Incorrect verdict %s=%s" % (arg, responce))
            properties[arg] = list(responces)
    if "expected" not in properties and "possible" not in properties:
        properties["expected"] = ["OK"]

def add_solution (path, args = None):
    if not args:
        args = []
    if not os.path.exists(path):
        raise PleaseException("There is no such file")
    if not os.getcwd() in os.path.abspath(path):
        raise PleaseException("Solution isn't in problem folder!")
    
    package_config = PackageConfig.get_config()
    abspath = os.path.abspath(path)
    if abspath == os.path.abspath(package_config["main_solution"]):
        raise PleaseException("Adding solution must not be equal to main")
    if package_config["solution"] is not None:
        for solve in package_config["solution"]:
            if os.path.abspath(solve["source"]) == abspath:
                raise PleaseException("There is already exist such solution")
            
    properties = get_dict_from_args(args)
    fix_args_user_mistakes(properties)

    new_config = config.Config("")
    new_config["source"] = os.path.relpath(path)
    for key, value in properties.items():
        new_config[key] = value
        
    package_config.set("solution", new_config, None, True)
    writepackage(package_config.get_text())
    log.info("Solution %s has been added successfully", path)
    
def change_solution (args):
    path = args[0]
    args = args[1:len(args)]
    config = PackageConfig.get_config()
    abspath = os.path.abspath(path)
    if config["solution"] is not None:
        for solve in config["solution"]:
            if os.path.abspath(solve["source"]) == abspath:
                properties = get_dict_from_args(args, True)
                fix_args_user_mistakes(properties)
                for key, value in properties.items():
                    solve[key] = value
                log.info("Properties have been changed")
                writepackage(config.get_text())
                return
    raise PleaseException("There is no such solution")

def del_props(args):
    path = args[0]
    args = args[1:len(args)]
    config = PackageConfig.get_config()
    abspath = os.path.abspath(path)
    if config["solution"] is not None:
        for solve in config["solution"]:
            if os.path.abspath(solve["source"]) == abspath:
                for key in args:
                    if key == "source":
                        raise PleaseException("Can't delete key 'source' from solution")
                    if key in solve:
                        del solve[key]
                    else:
                        log.warning("There is no key '" + key + "' in solution")
                writepackage(config.get_text())
                log.info("Properties have been deleted")
                return
    raise PleaseException("There is no such solution")

def add_checker_with_config (package_config, path):
    if not os.path.exists(path):
        raise PleaseException("There is no such file")
    #TODO: use relpath
    if not os.getcwd() in os.path.abspath(path):
        raise PleaseException("Checker isn't in problem folder!")
    package_config['checker'] = os.path.relpath(path)
    
def add_checker (path):
    package_config = PackageConfig.get_config()
    add_checker_with_config(package_config, path)
    package_text = package_config.get_text()
    writepackage(package_text)
    log.info("Checker %s has been set successfully", path)
    
def add_validator_with_config (package_config, path):
    if not os.path.exists(path):
        raise PleaseException("There is no such file")
    if not os.getcwd() in os.path.abspath(path):
        raise PleaseException("Validator isn't in problem folder!")
    package_config['validator'] = os.path.relpath(path)

def add_validator (path):
    package_config = PackageConfig.get_config()
    add_validator_with_config(package_config, path)
    package_text = package_config.get_text()
    writepackage(package_text)
    log.info("Validator %s has been set successfully", path)

def add_solution_with_config (package_config, path, expected= [], possible = []):
    #TODO: kill it. needed for correct import_from_polygon module work.
    config_file = config.Config("")
    config_file["source"] = os.path.relpath(path)
    if expected != []:
        config_file ["expected"] = expected
    if possible != []:
        config_file ["possible"] = possible
    package_config.set("solution", config_file, None, True)
