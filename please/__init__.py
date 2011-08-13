#!/usr/bin/python3
# -*- coding: utf-8 -*-

def main():
    from please import log
    from please.cleaner import cleaner
    from please.command_line.matcher import Matcher, MatcherException
    from please.command_line.template import Template
    from please.latex import latex_tools
    from please.executors.compiler import CompileError
    from please.executors.runner import RunnerError
    from please.template import problem_template_generator as problem_gen
    from please.add_source.add_source import add_solution, add_main_solution, add_checker, add_validator, add_solution_with_expected
    #from please.package import config
    from please import tags
    from please.solution_tester import check_solution
    import sys
    import logging
    from please.auto_TL.auto_tl import set_integer_tl
    from please.auto_TL.auto_tl import set_float_tl
    from please.command_line.generate_tests import generate_tests, generate_tests_with_tags
    from please.command_line.commands import print_help, print_lite_help
    from please.stress_tester import stress_tester
    from please.checkers.standard_checkers_utils import add_standard_checker_to_solution
    from please.todo import todo_generator
    from please.build_all.build_tools import build_all
    from please.solution_tester import package_config
    from please.export2ejudge.export import export2ejudge
    import os
    from please.import_from_polygon.import_problem_from_polygon import import_problem_from_polygon
    from please.import_from_polygon.create_problem import create_problem as import_polygon_package
    from please.answers_generator.answers_generator import AnswersGenerator
    from please.tests_answer_generator import tests_answer_generator
    from please.reports import generate_html_report
    
    mod_logger = logging.getLogger("please_logger")
    
    log.update_shortname()    
    
    todo = todo_generator.TodoGenerator()
    matcher = Matcher()
    matcher.add_handler(Template(["create", "problem", "#shortname"]), problem_gen.generate_problem, True)
    matcher.add_handler(Template(["export", "to", "ejudge", "contest", "#contest_id", "problem|problems", "@tasks"]), export2ejudge, True)
    matcher.add_handler(Template(["help"]), print_help, True)
    matcher.add_handler(Template(["generate", "statements", "@problem_names"]), latex_tools.generate_contest, True)
    matcher.add_handler(Template(["show", "todo", "#root_path"]), todo.get_todo, True)
    matcher.add_handler(Template(["todo", "#root_path"]), todo.get_todo, True)
    matcher.add_handler(Template(["import", "polygon", "problem", "#problem_letter", "from", "contest", "#contest_id"]), import_problem_from_polygon, True)
    matcher.add_handler(Template(["import", "polygon", "package", "#package"]), import_polygon_package, True)
    # If we are inside folder with  the problem, we have more handlers
    package_config = package_config.PackageConfig.get_config('.')
    in_problem_folder = (package_config != False)
    matcher.add_handler(Template(["validate", "tests"]), tests_answer_generator.TestsAndAnswersGenerator().validate, in_problem_folder)
    matcher.add_handler(Template(["clean"]), cleaner.Cleaner().cleanup, in_problem_folder)
    matcher.add_handler(Template(["show", "todo"]), todo.get_todo, in_problem_folder)
    matcher.add_handler(Template(["todo"]), todo.get_todo, in_problem_folder)
    matcher.add_handler(Template(["add", "tag|tags", "@tags"]), tags.add_tags, in_problem_folder)
    matcher.add_handler(Template(["set", "standard", "checker", "#checker"]), add_standard_checker_to_solution, in_problem_folder)
    matcher.add_handler(Template(["add", "solution", "#path", "expected:", "@expected_list", "possible:", "@possible_list"]), add_solution, in_problem_folder)
    matcher.add_handler(Template(["add", "solution", "#path", "with", "@expected_list"]), add_solution_with_expected, in_problem_folder)
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
    matcher.add_handler(Template(["generate", "answers"]), AnswersGenerator.generate_without_arguments, in_problem_folder)
    matcher.add_handler(Template(["stress", "test", "#solution", "#generator"]), stress_tester.StressTester(config = package_config), in_problem_folder)
    matcher.add_handler(Template(["stress", "test", "#solution", "#correct_solution", "#generator"]), stress_tester.StressTester(config = package_config), in_problem_folder)
    matcher.add_handler(Template(["check", "solutions"]), check_solution.check_multiple_solution, in_problem_folder)
    matcher.add_handler(Template(["check", "solution", "#path"]), check_solution.check_solution, in_problem_folder)
    matcher.add_handler(Template(["check", "main", "solution"]), check_solution.check_main_solution, in_problem_folder)
    matcher.add_handler(Template(["generate", "html", "report"]), generate_html_report.generate_html_report, in_problem_folder)

    if len(sys.argv) == 1:
        print_lite_help(package_config)
    else:
        # Get the command line arguments (exclude the first one - it's program's name)
        args = sys.argv[1:]
        # Run the function that is matched to the arguments entered
        try:
            matcher.matches(args)
        except MatcherException as ex:
            print(str(ex))
            print_lite_help(package_config)
        except CompileError as ex:
            log = logging.getLogger("please_logger.executors.compiler")
            log.error("CompilerError: " + str(ex))
        except RunnerError as ex:
            pass
        except OSError as ex:
            log = logging.getLogger("please_logger")
            log.error("OSError: " + str(ex))
