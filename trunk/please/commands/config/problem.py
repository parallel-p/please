
TL = ['TL', 'tl', 'timelimit', 'time-limit', 'time_limit']
ML = ['ML', 'ml', 'memorylimit', 'memory-limit', 'memory_limit']

def generate_tests(tags = []):
    '''gen[erate] tests [with tag[s] tags...]
    Generate tests for a problem, either everything or just with certain tags.'''
    from please.tests_answers_generator import generate, generate_all
    if tags:
        generate(tags)
    else:
        generate_all()

def generate_statement():
    '''gen[erate] statement|pdf
    Generate a statement for a problem.'''
    from please.latex import latex_tools
    latex_tools.generate_problem()

def generate_answers():
    '''gen[erate] ans[wers]
    Generate answers for tests.'''
    from please.answers_generator import generate_answers
    generate_answers()

def validate_tests():
    '''val[idate] [tests]
    Validate all tests for a problem.'''
    from please.tests_answers_generator import validate
    tg = TestsAndAnswersGenerator()
    tg.validate()

def set_validator(path):
    '''set val[idator] /path
    Add a program to validate tests for a problem.'''
    from please.add_source import add_validator
    add_validator(path)

def stress_test(solution, correct = None, generator):
    '''stress $solution [against $correct] with $generator
    Stress a solution (possibly against correct one) using generator.'''
    # О-очень плохой calling convenience!
    # Я думал, гораздо лучше будет это всё.
    # Non-native, do not worry, it's knda untranslatable joke.
    from please.stress_test.stress_test import StressTester
    StressTester()(solution, generator, correct)

def set_param(parameter, value):
    '''set problem $parameter to $value
    Configure problem's parameter to be a value.
    Possible parameters are:
        name
        input
        output
        TL (or other abbreviation)
        ML (or other abbreviation)'''
    from please.package.package_config import PackageConfig
    if parameter in TL:
        parameter = 'time-limit'
    elif parameter in ML:
        parameter = 'memory-limit'
    else:
        if parameter not in {'name', 'input', 'output'}:
            raise PleaseException('unsupported parameter: {}'.format(parameter))
    cfg = PackageConfig.get_config()
    if cfg is None:
        raise PleaseException('problem package not found')
    cfg[parameter] = value
        
def set_standard_checker(checker = None):
    '''set standard|std checker [/path]
    Set a standard checker to be a checker for a problem
    (or print available ones).'''
    from please.checkers.standard_checker_utils import (add_standard_checker_to_solution,
                                                        print_standard_checkers)
    if checker is None:
        print_standard_checkers()
    else:
        add_standard_checker_to_solution(checker)

# TODO something with these one-liners.
# For example, more documentation.

def set_checker(path):
    '''set checker /path
    Assign a custom checker to a problem.'''
    from please.add_source import add_checker
    add_checker(path)

def set_main_solution(path):
    '''set main solution /path
    Add a solution and mark it as main.'''
    from please.add_source import add_main_solution
    add_main_solution(path)

def add_solution(path, args):
    '''add sol[ution] /path args...
    Add a solution to a problem.'''
    from please.add_source import add_solution
    add_solution(path, args)

def del_solution(path):
    '''del[ete] sol[ution] path
    Delete a solution from a problem.'''
    from please.add_source import del_solution
    del_solution(path)

def change_props(path, args):
    '''change prop[erties] of /path to args...
    Change properties for certain solution.'''
    from please.add_source import change_properties
    change_properties(path, args)

def del_props(path):
    '''del[ete] prop[erties] of /path
    Delete all properties assigned to a certain solution.'''
    from please.add_source import del_props
    del_props(path)

def check_solutions(solution):
    '''check $solution
    solution may be a path pointing to a certain solution,
    or `main', or `all'.'''
    from please.solution_tester import check_solution
    if solution == 'main':
        check_solution.check_main_solution()
    elif solution == 'all':
        check_solution.check_all_solutions()
    else:
        check_solution.check_solution(solution)


def compute(type = 'float', limit):
    '''compute [$type] $limit
    Compute an execution limit for solutions.
    Supported types is integer and float.
    Supported execution limit is only TL, sorry for the inconvenience.'''
    if type not in {'float', 'int', 'integer'}:
        raise PleaseException('Unsupported limit type: {}'.format(type))
    if limit in ML:
        raise PleaseException('Computing memory limits is not supported now')
    elif limit in TL:
        from please.auto_TL import auto_tl
        if type == 'float':
            auto_tl.set_float_tl()
        else:
            auto_tl.set_integer_tl()
    else:
        raise PleaseException('I am sophisticated, but is not able to compute everything!')
