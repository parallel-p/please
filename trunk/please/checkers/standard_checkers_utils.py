import os
import logging
import shutil
from .. import globalconfig
from ..solution_tester import package_config
from ..utils.writepackage import writepackage
from ..add_source.add_source import add_checker

log = logging.getLogger("please_logger.checkers.standard_checker_utils")

class AddStandartCheckerError (Exception) :
    pass

def print_standard_checkers():
    opened_config = package_config.PackageConfig.get_config()
    checkers_dir = os.path.join(globalconfig.root, globalconfig.checkers_dir)
    dirList=os.listdir(checkers_dir)
    filelist = []
    for fname in dirList:
        if fname.endswith('.cpp'):
           filelist += [fname[:-4]]
    log.warning('standart checkers available: ' + ', '.join(filelist))

def add_standard_checker_to_solution (checker):
    """
    Description : 
       If checker is found in global directory then this function
       will write the global path to the checker into config file.
    """
    opened_config = package_config.PackageConfig.get_config()
    if not checker.endswith('.cpp'):
        checker_name = checker + ".cpp"
    else:
        checker_name = checker
    checker_global_path = os.path.join(globalconfig.root, globalconfig.checkers_dir, checker_name)
    
    if not os.path.exists(checker_global_path) :
        print_standard_checkers()
        raise AddStandartCheckerError("Standart checker " + checker_name + " not found!")
    else:
        if not os.path.exists('testlib.h') :
            shutil.copy(os.path.join(globalconfig.root, globalconfig.checkers_dir, 'testlib.h'), 'testlib.h')
        add_checker(checker_global_path)
