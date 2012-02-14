#!/usr/bin/python3
import os
import sys
import logging

from please import globalconfig
from please.log import logger
from please.package import config
from please.command_line.matcher import Matcher
from please.executors import trash_remover
from please import command_line_config
from please.tests_answer_generator import tests_answer_generator
from please.utils.exceptions import PleaseException, MatcherException

def determinate_location():
    """
        Returns True is location is root of the problem
    """
    from please.solution_tester import package_config
    startdir = current_dir = os.getcwd()
    prev_dir = '?'
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
    return in_problem_folder, startdir

def main():
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

        command_line_config.add_stress_test_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_contest_operations(matcher,
            active=not in_problem_folder)

        command_line_config.add_aggregate_operations(matcher,
            active=in_problem_folder)

        command_line_config.add_export_operations(matcher)
    
        command_line_config.add_easter_eggs_operations(matcher)
    
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
        
if __name__ == "__main__":
    print("develop")
    main()

