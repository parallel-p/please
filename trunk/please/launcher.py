#!/usr/bin/python3
import os
import sys

from . import globalconfig
from .log import logger
from .command_line.matcher import Matcher
from .executors import trash_remover
from . import command_line_config
from .utils.exceptions import PleaseException, MatcherException
from .package import package_config
from .commands import get_please_matcher

def determinate_location():
    """
        Returns True is location is root of the problem
    """
    startdir = current_dir = os.getcwd()
    prev_dir = None
    pkg = package_config.PackageConfig.get_config()
    while current_dir != prev_dir and pkg is None:
        prev_dir = current_dir
        os.chdir('..')
        current_dir = os.getcwd()
        pkg = package_config.PackageConfig.get_config()
    if pkg is None:
        os.chdir(startdir)
    in_problem_folder = (pkg is not None)
    globalconfig.in_problem_folder = in_problem_folder
    if in_problem_folder:
        globalconfig.problem_folder = current_dir
    return in_problem_folder, startdir

def legacy_main():
    try:
        in_problem_folder, startdir = determinate_location()
        matcher = Matcher()
        matcher.startdir = startdir
        command_line_config.add_help_commands(matcher)

        command_line_config.add_creation_operations(matcher,
            active=not in_problem_folder)

        command_line_config.add_solution_modifications(matcher,
            active=in_problem_folder)

        command_line_config.add_import_opertions(matcher,
            active=not in_problem_folder)

        command_line_config.add_todo_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_tags_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_generate_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_checking_solution_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_computing_tl_functions(matcher,
            active=in_problem_folder)

        command_line_config.add_validate_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_checker_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_problem_config_modification_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_zip_operation(matcher,
                                              active = in_problem_folder)

        command_line_config.add_stress_test_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_contest_operations(matcher,
            active=not in_problem_folder)

        command_line_config.add_aggregate_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_export_operations(matcher)
    
        command_line_config.add_easter_eggs_operations(matcher)

        command_line_config.add_simple_bridge(matcher)
    
        if len(sys.argv) == 1:
            logger.info("Type 'please commands' to show all available commands or 'please help' to show them with detailed description")
        else:
            # Get the command line arguments (exclude the first one - it's program's name)
            args = sys.argv[1:]
            # Run the function that is matched to the arguments entered
            
            try:
                matcher.matches(args)
            except MatcherException as ex:
                logger.error("MatcherException: " + str(ex))
                logger.info("Type 'please commands' to show all available commands or 'please help' to show them with detailed description")
            except IOError as ex:
                logger.error("IOError: " + str(ex))
            except PleaseException as ex:
                logger.error("Please error: %s" % str(ex))
            except Exception as ex:
                logger.error("Unknown error: " + str(ex))
                raise ex
            
        #TODO: why we delete logs in this case?
        #because we didn't do anything useful 
        if(not globalconfig.in_problem_folder):
            trash_remover.remove_logs_in_depth(out=False, depth=False)
    
    except IOError as ex:
        print("IOError: " + str(ex))


def please_excepthook(exc_type, exc_value, exc_tb):
    if issubclass(exc_type, PleaseException):
        logger.error('Please error: {}'.format(exc_value))
    elif issubclass(exc_type, IOError):
        logger.error('I/O error: {}'.format(exc_value))
    else:
        logger.error('Unknown error: {}: {}'.format(exc_type.__name__, exc_value))
    if globalconfig.DEBUG_MODE:
        traceback.print_exception(exc_type, exc_value, exc_tb)
    sys.exit(1)

def main():
    # searching for package directory
    curdir = os.getcwd()
    lastdir = None
    while lastdir != curdir:
        config = package_config.PackageConfig.get_config(curdir)
        if config is not None:
            break
        lastdir = curdir
        curdir = os.path.dirname(curdir)
    if config is not None:
        globalconfig.problem_folder = curdir
   
    sys.excepthook = please_excepthook
    args = sys.argv[1:]
    if not args:
        logger.info("type `please help' for list of commands")
        sys.exit(2)
    else:
        matcher = get_please_matcher()
        if not matcher.call(args):
            logger.error('command not recognized')
            logger.error("try `please help'")
            sys.exit(2)
        else:
            sys.exit(0)

if __name__ == "__main__":
    #legacy_main()
    #sys.exit()
    main()
    
