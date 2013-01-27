import os.path
from . import contest
from ..latex import latex_tools
from ..exporter import exporter
from ..package import package_config
from ..log import logger
from ..utils.exceptions import PleaseException
from ..globalconfig import contest_template

def get_contest_config(name, path = '.'):
    return os.path.join(path, contest_template.format(name))

def get_contest(name, ok_if_not_exists = False):
    return contest.Contest(get_contest_config(name), ok_if_not_exists)

def add_problems_to_contest(contest, problems, ids = None):
    """
        Adds some problems to contest, where <problems> is list returned by matcher
        for example, problems: ['sloniki', 'grader', 'as', 'A,B']
    """
    r = []
    if ids:
        if len(problems) != len(ids):
            raise PleaseException("Problems count (%d) does not match IDs count (%d)" % (len(problems), len(ids)))
        problems = zip(problems, ids)
    else:
        problems = zip(problems, [False] * len(problems))

    for problem, id in problems:
        contest.problem_add(problem, id)
        r.append(problem)

    return r

def remove_problems_from_contest(contest, problems):
    r = [] # cannot use yield becase all problems must be removed before other actions
    for problem in problems:
        if problem in contest:
            contest.problem_remove(problem)
        elif contest.problem_find(problem) is not None:
            problem = contest.problem_find(problem)
            contest.problem_remove(problem)
        else:
            raise PleaseException("Problem %s is not found" % problem)
        r.append(problem)
    return r

def write_contest(name, contest):
    """ Saves contest to its .contest file """
    contest.config.write()

def command_create_contest(name, problems):
    if os.path.exists(get_contest_config(name)):
        logger.error('Contest with config %s already exists' % get_contest_config(name))
        return
    new_contest = get_contest(name, True)
    add_problems_to_contest(new_contest, problems)
    write_contest(name, new_contest)
    logger.info("created contest %s with %d problems" % (name, len(problems)))

def command_add_problems(name, problems, problems_as = []):
    current_contest = get_contest(name)
    r = add_problems_to_contest(current_contest, problems, problems_as)
    write_contest(name, current_contest)
    if len(r) == 1:
        logger.info("added problem %s to contest" % r[0])
    else:
        logger.info("added %s problems to contest: %s" % (len(r), ','.join(r)))

def command_remove_problems(name, problems):
    current_contest = get_contest(name)
    r = remove_problems_from_contest(current_contest, problems)
    write_contest(name, current_contest)
    if len(r) == 1:
        logger.info("removed problem %s from contest" % r[0])
    else:
        logger.info("removed %d problems from contest: %s" % (len(r), ','.join(r)))

def command_generate_statement(name):
    current_contest = get_contest(name)
    problems = []
    for problem in current_contest.config['problem']:
        config = package_config.PackageConfig.get_config(problem['path'])
        # TODO: check if config is None
        config['id'] = problem['id']
        problems.append(problem['path'])
    template_vars = {}
    for ind, val in current_contest.config['statement'].items():
        template_vars[ind] = val
    latex_tools.generate_contest(problems, template_vars['template'], template_vars, file = name)

def command_export(name, where, contest):
    current_contest = get_contest(name)
    problems = []
    print(where, contest, current_contest)
    for problem in current_contest.config['problem']:
        config = package_config.PackageConfig.get_config(problem['path'])
        # TODO: check if config is None
        config['id'] = problem['id']
        problems.append(problem['path'])
    exporter.export(where, contest, problems)

def command_set_parameter( name, key, value ):
    if key not in ('name', 'id_method', 'statement.name', 'statement.date', 'statement.location', 'statement.template'):
        raise PleaseException("An unknown contest parameter: %s" % key)
    key = key.split('.')
    contest = get_contest(name)
    config = contest.config
    for x in key[:-1]:
        config = config[x]
    config[key[-1]] = value
    write_contest(name, contest)
    logger.info("Modified %s in contest \"%s\"" % (' '.join(key), name))

