from please.utils.exceptions import PleaseException
from please import globalconfig
# Do not add too much above.
# Less is better.

class MonkeyPatch:
    '''Monkey patch for alias ids in contest.'''
    def __init__(self, contest):
        from please.package.package_config import PackageConfig
        self.problems = {}
        for problem in contest.config['problem']:
            path = problem['path']
            config = PackageConfig.get_config(path)
            self.problems[path] = config, config['id'], problem['id']
        
    def __enter__(self):
        for config, config_id, problem_id in self.problems:
            config['id'] = problem_id
        return list(self.problems.keys())

    def __exit__(self, *idontcare):
        for config, config_id, problem_id in self.problems:
            config['id'] = config_id

def _get_contest_config(name):
    if globalconfig.problem_folder != None:
        raise PleaseException('Cannot work with contests in problem folder')
    return globalconfig.contest_template.format(name)

def _load_contest(name, can_create = False):
    from please.contest.contest import Contest
    contest_file = _get_contest_config(name)
    return Contest(contest_file, can_create)



def add_problems(contest, problems, ids = []):
    '''add problem[s] problems... to $contest [as ids...]
    Add several problems to a contest.'''
    from itertools import repeat
    ids = ids or repeat(None)
    contest = _load_contest(contest, True)
    for problem, id in zip(problems, ids):
        contest.problem_add(problem, id)

def delete_problems(contest, problems):
    '''del[ete] problem[s] problems... from $contest
    Delete several problems from contest.'''
    contest = _load_contest(contest)
    for problem in problems:
        contest.problem_remove(problem)

def generate_statement(name):
    '''gen[erate] [contest] $name statements|pdf
    Generate statements for contest out of problems' statements.'''
    from please.latex import latex_tools
    from please.package.package_config import PackageConfig
    contest = _load_contest(name)
    template_vars = dict(current_contest.config['statement'])
    with MonkeyPatch(contest) as problems:
        latex_tools.generate_contest(problems, template_vars['template'],
                                     template_vars, file = name)

def export(name, where, alias):
    '''export $name to /where as $alias
    '''
    from please.exporter import export
    contest = _load_contest(name)
    with MonkeyPatch(contest) as problems:
        export(where, alias, problems)

def set_parameter(contest, parameter, value):
    '''set contest $contest $parameter to $value
    Set the parameter of contest to be a value.'''
    if parameter == 'problem':
        raise PleaseException('Cannot be done that way. '
                              'Please use add problems / delete problems.')
    keys = parameter.split('.')
    contest = _load_contest(contest)
    config = contest.config
    try:
        for key in keys[:-1]:
            config = config[key]
    except KeyError:
        raise PleaseException('Unknown parameter: {}'.format(parameter))
    else:
        config[keys[-1]] = value
        contest.save()

def create_contest(contest, name = '', problems = []):
    '''create contest $contest [with name $name] [of problems problems...]
    Create a new contest. It is really not that much - just a config
    file. Contests are used to assemble problems together and are able
    to automatically generate statements for themselves.
    `contest' argument is for internal name of contest. It must be unique.
    `name' argument is for contest printable name. It may appear in statements.
    `problems' argument are paths to problems configured with please.
    You are able add or delete some problems to contest later.'''
    from os.path import exists
    if exists(_get_contest_config(contest)):
        raise PleaseException('Sorry, but there is already contest configured '
                              'with this name. Use `add problems\' or `delete '
                              'problems\' to modify it, or try another name.')
    contest = _load_contest(name, True)
    for problem in problems:
        contest.problem_add(problem, None)
    contest.save()


