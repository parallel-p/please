import os.path
import logging
from . import contest
from ..latex import latex_tools
from ..exporter import exporter
from ..solution_tester import package_config
from ..log import logger

CONTEST_FILE = "%s.contest"

def get_contest_config(name, path = '.'):
    return os.path.join(path, CONTEST_FILE % name)

def get_contest(name, ok_if_not_exists = False):
    return contest.Contest(get_contest_config(name), ok_if_not_exists)

def add_problems_to_contest(contest, problems):
    """
        Adds some problems to contest, where <problems> is list returned by matcher
        for example, problems: ['sloniki', 'grader', 'as', 'A,B']
    """
    if len(problems) >= 3 and problems[-2] == "as":
        ids = problems[-1].split(',')
        # TODO: assert len(problems) == len(ids)
        problems = zip(problems, ids)
    else:
        problems = zip(problems, [False] * len(problems))

    for problem, id in problems:
        contest.problem_add(problem, id)

def remove_problems_from_contest(contest, problems):
    for problem in problems:
        if problem in contest:
            contest.problem_remove(problem)
        elif contest.problem_find(problem) is not None:
            contest.problem_remove(contest.problem_find(problem))
        # TODO else raise somthing

def write_contest(name, contest):
    """ Saves contest to its .contest file """
    with open(get_contest_config(name), 'w') as f:
        f.write(contest.config.get_text())

def command_create_contest(name, problems):
    if os.path.exists(get_contest_config(name)):
        logger.error('Contest with config %s already exists' % get_contest_config(name))
        return
    new_contest = get_contest(name, True)
    add_problems_to_contest(new_contest, problems)
    write_contest(name, new_contest)

def command_add_problems(name, problems, problems_as = []):
    current_contest = get_contest(name)
    add_problems_to_contest(current_contest, problems + problems_as)
    write_contest(name, current_contest)

def command_remove_problems(name, problems):
    current_contest = get_contest(name)
    remove_problems_from_contest(current_contest, problems)
    write_contest(name, current_contest)

def command_generate_statement(name):
    current_contest = get_contest(name)
    problems = []
    for problem in current_contest.config['problem']:
        config = package_config.PackageConfig.get_config(problem['path'])
        config['id'] = problem['id']
        print(config['id'])
        problems.append(problem['path'])
    template_vars = {}
    for ind, val in current_contest.config['statement'].items():
        template_vars[ind] = val
    latex_tools.generate_contest(problems, template_vars['template'], template_vars)

def command_export(name, where, contest):
    current_contest = get_contest(name)
    problems = []
    for problem in current_contest.config['problem']:
        config = package_config.PackageConfig.get_config(problem['path'])
        config['id'] = problem['id']
        problems.append(problem['path'])
    exporter.export(where, contest, problems)
