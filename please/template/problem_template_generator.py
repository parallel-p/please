from os import mkdir
from os.path import exists
import os.path
from .. import globalconfig as global_config
from .template_utils import get_template_full_path
from .statement_template_generator import generate_description, generate_statement
from .source_code_file_generator import generate_checker, generate_solution, generate_validator
from ..package.config import Config as package_config
from . import info_generator
import logging
import shutil

log = logging.getLogger("please_logger.template.problem_template_generator")

class ProblemExistsError(IOError):
    def __init__(self, shortname):
        self.__shortname=shortname
    def __str__(self):
        return "%s already exists" % self.__shortname

def generate_package(name, replaces, shortname):
    ''' Generates {default}.package file '''
    # maybe we will have templates not only for default.package?
    default_package_path = get_template_full_path(name) or get_template_full_path('default.package')

    if default_package_path:
        default_package = open(default_package_path, 'r', encoding = "UTF8")
        package = package_config(default_package.read())
        default_package.close()
    else:
        package = package_config("")

    new_package = open(os.path.join(shortname, name), 'w', encoding = 'UTF8')

    for replace, data in replaces.items():
        package[replace] = data

    new_package.write(package.get_text())
    new_package.close()

def generate_problem_advanced(shortname, human_language, programming_language):
    ''' Generates file structure of problem (templates (checker, validator, etc) and default.package) '''
    if exists(shortname):
        raise ProblemExistsError(shortname)

    mkdir(shortname)

    statement_path = os.path.join(shortname, global_config.statements_dir)
    tests_path = os.path.join(shortname, 'tests')
    solutions_path = os.path.join(shortname, global_config.solutions_dir)

    # make dirs
    mkdir(statement_path)
    mkdir(tests_path)
    mkdir(solutions_path)

    replaces = {'please_version': str(global_config.please_version),
                'shortname': shortname,
                'description': global_config.statements_dir + '/' + generate_description(statement_path, human_language),
                'statement': global_config.statements_dir + '/' + generate_statement(statement_path, human_language),
                'validator': generate_validator(shortname, programming_language),
                'checker': generate_checker(shortname, programming_language),
                'main_solution': global_config.solutions_dir + '/' + generate_solution(solutions_path, programming_language)}

    generate_package('default.package', replaces, shortname)

    # generate empty tests.please
    open(os.path.join(shortname, 'tests.please'), 'w').close()

    # copy testlib.h & testlib.pas
    testlib_h = get_template_full_path("testlib.h")
    testlib_pas = get_template_full_path("testlib.pas")
    if testlib_h is not None:
        shutil.copy(testlib_h, os.path.join(shortname, 'testlib.h'))
    if testlib_pas is not None:
        shutil.copy(testlib_pas, os.path.join(shortname, 'testlib.pas'))

def generate_problem(shortname, handle_exception=True):
    try:
        generate_problem_advanced(shortname,
                              global_config.default_human_language,
                              global_config.default_programming_language)
        info_generator.create_time_file(shortname)
        log.info("Problem %s created successfully", str(shortname))
    except ProblemExistsError as Error:
        log.error(str(Error))
