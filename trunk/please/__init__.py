#!/usr/bin/python3
# -*- coding: utf-8 -*-
from please import globalconfig
from please.solution_tester.check_solution import SolutionNotFoundException
from please.add_source.add_source import AddSourceError
from please.log import logger
from please.package import config
from please.command_line.matcher import Matcher, MatcherException
from please.executors.compiler import CompileError
from please.executors.runner import RunnerError
from please.executors import trash_remover
from please import command_line_config
from please.tests_answer_generator import tests_answer_generator
from please.utils.exception import Sorry
import sys
import logging

def determinate_location():
    """
        Returns True is location is root of the problem
    """
    # If we are inside folder with  the problem, we have more handlers
    from please.solution_tester import package_config
    pkg = package_config.PackageConfig.get_config()
    in_problem_folder = (pkg is not None)
    globalconfig.in_problem_folder = in_problem_folder
    return in_problem_folder

def main():
    try:
        in_problem_folder = determinate_location()
        matcher = Matcher()
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
            except RunnerError as ex:
                logger.error("RunnerError: " + str(ex))
            except CompileError as ex:
                logger.error("CompileError: " + str(ex))
            except OSError as ex:
                logger.error("OSError: " + str(ex))
            except config.ConfigException as ex:
                logger.error("ConfigError: " + str(ex))
            except IOError as ex:
                logger.error("IOError: " + str(ex))
            except EnvironmentError as ex:
                logger.error("EnvironmentError: " + str(ex))
            except tests_answer_generator.ValidatorError as ex:
                logger.error("ValidatorError: " + str(ex))
            except AddSourceError as ex:
                logger.error("AddSourceError: " + str(ex))
            except SolutionNotFoundException as ex:
                logger.error("SolutionNotFoundException: " + str(ex))
            except Sorry as ex:
                logger.error("Please error: %s" % str(ex))
            except Exception as ex:
                logger.error("Unknown error: " + str(ex))
                raise ex
       
        #TODO: why we delete logs in this case? 
        if(not globalconfig.in_problem_folder):
            trash_remover.remove_logs_in_depth(out=False, depth=False)
    
    except IOError as ex:
        print("IOError: " + str(ex))
        
if __name__ == "__main__":
    main()

