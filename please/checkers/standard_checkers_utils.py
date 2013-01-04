import os
import logging
import shutil
import filecmp
from .. import globalconfig
from ..package import package_config
from ..add_source.add_source import add_checker
from ..utils.exceptions import PleaseException
from ..todo.todo_generator import TodoGenerator

log = logging.getLogger("please_logger.checkers.standard_checker_utils")


def print_standard_checkers():
    #opened_config = package_config.PackageConfig.get_config()
    # TODO: check if opened_config is None
    # opened_config is unused here, remove it
    checkers_dir = os.path.join(globalconfig.root, globalconfig.checkers_dir)
    dirList = os.listdir(checkers_dir)
    filelist = []
    for fname in dirList:
        if fname.endswith('.cpp'):
            filelist += [fname[:-4]]
    log.warning('Standard checkers available: ' + ', '.join(filelist))
    log.warning('For more detailed information look at wiki on http://code.google.com/p/please')


def __checker_global_dir():
    return os.path.join(globalconfig.root, globalconfig.checkers_dir)


def is_default_checker(checker, config):
    if not os.path.exists(checker):
        #checker is set to invalid path
        return False
    checker_global_dir = __checker_global_dir()
    candidate_path = os.path.join(checker_global_dir, os.path.basename(checker))
    if os.path.exists(candidate_path) and filecmp.cmp(checker, candidate_path, shallow=False):
        #checker is default and not modified
        return True

    if not TodoGenerator.is_item_modified("checker", config):
        return True

    return False


def clear_old_default_checker(config):
    current_checker = config["checker"]
    if is_default_checker(current_checker, config):
        log.info("Delete previous checker %s" % current_checker)
        os.remove(current_checker)


def add_standard_checker_to_solution(checker):
    """
    Description :
       If checker is found in global directory then this function
       will write the global path to the checker into config file.
    """
    config = package_config.PackageConfig.get_config()
    if not checker.endswith('.cpp'):
        checker_name = checker + ".cpp"
    else:
        checker_name = checker
    checker_global_path = os.path.join(__checker_global_dir(), checker_name)
    if not os.path.exists(checker_global_path):
        print_standard_checkers()
        raise PleaseException("Standard checker " + checker_name + " not found!")
    else:
        clear_old_default_checker(config)
        shutil.copy(checker_global_path, checker_name)
        if not os.path.exists('testlib.h'):
            shutil.copy(os.path.join(globalconfig.root, globalconfig.checkers_dir, 'testlib.h'),
                    'testlib.h')
        add_checker(checker_name)
        return checker_name
