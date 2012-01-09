#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Sorry(Exception):
    def __init__( self, message ):
        self.__message = message
    def __str__( self ):
        return "sorry: %s" % self.__message

def main():
    try:
        from please.contest import commands as contest_commands
        from please.solution_tester.check_solution import SolutionNotFoundException
        from please.add_source.add_source import AddSourceError
        from please.log import logger
        from please.package import config
        from please.cleaner import cleaner
        from please.command_line.matcher import Matcher, MatcherException
        from please.command_line.template import Template
        from please.latex import latex_tools
        from please.executors.compiler import CompileError
        from please.executors.runner import RunnerError
        from please.template import problem_template_generator as problem_gen
        from please.add_source.add_source import del_props, del_solution, add_solution, add_main_solution, add_checker, add_validator, change_solution
        from please import tags
        from please.solution_tester import check_solution
        from please.well_done import well_done
        from please import globalconfig
        from please.executors import trash_remover
        import sys
        import logging
        from please.test_config_parser import parser
        from please.auto_TL.auto_tl import set_integer_tl
        from please.auto_TL.auto_tl import set_float_tl
        from please.command_line.generate_tests import generate_tests, generate_tests_with_tags
        from please.command_line.commands import print_help, print_lite_help
        from please.stress_tester import stress_tester
        from please.checkers.standard_checkers_utils import add_standard_checker_to_solution
        from please.checkers.standard_checkers_utils import print_standard_checkers
        from please.todo import todo_generator
        from please.build_all.build_tools import build_all
        from please.solution_tester import package_config
        import os
        from please.import_from_polygon.import_problem_from_polygon import import_problem_from_polygon
        from please.import_from_polygon.create_problem import create_problem as import_polygon_package
        from please.import_from_polygon.create_contest import create_contest as import_polygon_contest
        from please.answers_generator.answers_generator import AnswersGenerator
        from please.tests_answer_generator import tests_answer_generator
        from please.reports import generate_html_report
        from please.exporter.exporter import export
    
        matcher = Matcher()
        matcher.add_handler(Template(["create", "problem", "#shortname"]), problem_gen.generate_problem, True)
        #matcher.add_handler(Template(["export", "to", "ejudge", "contest", "#contest_id", "problem|problems", "@tasks"]), export2ejudge, True)
        matcher.add_handler(Template(["export", "to", "#server_name", "contest", "#contest_id", "problem|problems", "@problems"]), export, True)
        matcher.add_handler(Template(["help"]), print_help, True)
        matcher.add_handler(Template(["commands"]), print_lite_help, True)
        #matcher.add_handler(Template(["generate", "statements", "@problem_names"]), latex_tools.generate_contest, True)
        matcher.add_handler(Template(["import", "polygon", "problem", "#problem_letter", "from", "contest", "#contest_id"]), import_problem_from_polygon, True)
        matcher.add_handler(Template(["import", "polygon", "package", "#package"]), import_polygon_package, True)
        # If we are inside folder with  the problem, we have more handlers
        package_config = package_config.PackageConfig.get_config()
        in_problem_folder = (package_config is not None)
        globalconfig.in_problem_folder = in_problem_folder
        #matcher.add_handler(Template(["well", "done"]), well_done.WellDoneCheck().all, in_problem_folder)
        #matcher.add_handler(Template(["delete", "problem", "#shortname"]), svn.delete_problem, in_problem_folder)
        matcher.add_handler(Template(["validate", "tests"]), tests_answer_generator.TestsAndAnswersGenerator().validate, in_problem_folder)
        matcher.add_handler(Template(["clean"]), cleaner.Cleaner().cleanup, in_problem_folder)
        matcher.add_handler(Template(["show", "todo"]), todo_generator.TodoGenerator.get_todo, in_problem_folder)
        matcher.add_handler(Template(["todo"]), todo_generator.TodoGenerator.get_todo, in_problem_folder)
        matcher.add_handler(Template(["add", "tag|tags", "@tags"]), tags.add_tags, in_problem_folder)
        matcher.add_handler(Template(["set", "standard", "checker", "#checker"]), add_standard_checker_to_solution, in_problem_folder)
        matcher.add_handler(Template(["set", "standard", "checker"]), print_standard_checkers, in_problem_folder)
        matcher.add_handler(Template(["add", "solution", "@args"]), add_solution, in_problem_folder)
        matcher.add_handler(Template(["delete|del", "solution", "#path"]), del_solution, in_problem_folder)
        matcher.add_handler(Template(["change", "prop|properties", "@args"]),change_solution, in_problem_folder)
        matcher.add_handler(Template(["delete|del", "prop|properties", "@args"]),del_props, in_problem_folder)
        matcher.add_handler(Template(["set", "checker", "#path"]), add_checker, in_problem_folder)
        matcher.add_handler(Template(["set", "main", "solution", "#path"]), add_main_solution, in_problem_folder)
        matcher.add_handler(Template(["set", "validator", "#path"]), add_validator, in_problem_folder)
        matcher.add_handler(Template(["set", "problem", "name", "#name"]), tags.set_name, in_problem_folder)
        matcher.add_handler(Template(["build", "all"]), build_all, in_problem_folder)
        matcher.add_handler(Template(["show", "tags"]), tags.show_tags, in_problem_folder)
        matcher.add_handler(Template(["compute", "TL"]), set_float_tl, in_problem_folder)
        matcher.add_handler(Template(["compute", "integer", "TL"]), set_integer_tl, in_problem_folder)
        matcher.add_handler(Template(["clear", "tags"]), tags.clear_tags, in_problem_folder)
        matcher.add_handler(Template(["generate", "tests", "with", "tag|tags", "@tags"]), generate_tests_with_tags, in_problem_folder)
        matcher.add_handler(Template(["generate", "tests"]), generate_tests, in_problem_folder)
        matcher.add_handler(Template(["generate", "statement"]), latex_tools.generate_contest, in_problem_folder)
        matcher.add_handler(Template(["generate", "answers"]), AnswersGenerator.generate, in_problem_folder)
        matcher.add_handler(Template(["stress", "test", "#solution", "#generator"]), stress_tester.StressTester(config = package_config), in_problem_folder)
        matcher.add_handler(Template(["stress", "test", "#solution", "#correct_solution", "#generator"]), stress_tester.StressTester(config = package_config), in_problem_folder)
        matcher.add_handler(Template(["check", "solutions"]), check_solution.check_multiple_solution, in_problem_folder)
        matcher.add_handler(Template(["check", "solution", "#path"]), check_solution.check_solution, in_problem_folder)
        matcher.add_handler(Template(["check", "main", "solution"]), check_solution.check_main_solution, in_problem_folder)
        #matcher.add_handler(Template(["generate", "html", "report"]), generate_html_report.generate_html_report, in_problem_folder)
    
        # Contests support
        matcher.add_handler(Template(["create", "contest", "#name", "problems", "@problems"]), contest_commands.command_create_contest, True)
        matcher.add_handler(Template(["add", "@problems", "to", "#name", "@problems_as"]), contest_commands.command_add_problems, True)
        matcher.add_handler(Template(["add", "@problems", "to", "#name"]), contest_commands.command_add_problems, True)
        matcher.add_handler(Template(["remove", "@problems", "from", "#name"]), contest_commands.command_remove_problems, True)
        matcher.add_handler(Template(["generate", "statement", "for", "#name"]), contest_commands.command_generate_statement, True)
        matcher.add_handler(Template(["export", "#name", "to", "#where", "contest", "#contest"]), contest_commands.command_export, True)
        matcher.add_handler(Template(["set", "contest", "#name", "#key", "#value"]), contest_commands.command_set_parameter, True)
        matcher.add_handler(Template(["import", "polygon", "contest", "#name"]), import_polygon_contest, True)
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
            except Sorry as sorry:
                logger.error(str(sorry))
            except Exception as ex:
                logger.error("Unknown error: " + str(ex))
                raise ex
        
        if(not globalconfig.in_problem_folder):
            trash_remover.remove_logs_in_depth(out=False, depth=False)
    
    except IOError as ex:
        print("IOError: " + str(ex))
        
if __name__ == "__main__":
    main()

