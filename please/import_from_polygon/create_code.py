import os
import shutil
from ..package import config
from ..add_source import add_source

polygon2please_verdicts = {
    'main': (['OK'], []),
    'accepted': (['OK'], []),
    'memory-limit-exceeded': (['ML'], ['OK', 'WA', 'TL', 'RE', 'PE']),
    'time-limit-exceeded': (['TL'], ['OK', 'WA', 'ML', 'RE', 'PE']),
    'wrong-answer': (['WA'], ['OK', 'ML', 'TL', 'RE', 'PE']),
    'presentation-error': (['PE'], ['OK', 'WA', 'ML', 'TL', 'RE']),
    'rejected': ([], ['OK', 'WA', 'ML', 'TL', 'RE', 'PE']), #WARNING: uncorrect line
    'failed': (['CF'], ['OK', 'WA', 'ML', 'TL', 'RE', 'PE'])
    }

def __push_back(line, data)
    if line == '':
        return data
    else:
        return line + ', ' + str(data)
       
def copy_something(problem_config, problem_path, something_in_problem_path, \
                   something_path, something_name):
    shutil.copy(something_path, os.path.join(problem_path, something_in_problem_path))
    if not something_name is None:
        problem_config[something_name] = __push_back(problem_config[something_name], \
                                                     something_path)
    
def copy_validator(problem_config, problem_path, validator_path):
    cur_dir = os.getcwd()
    os.chdir(problem_path)
    add_source.add_validator_with_config(problem_config, os.path.join(cur_dir, validator_path))
    os.chdir(cur_dir)
    
def copy_checker(problem_config, problem_path, checker_path):
    cur_dir = os.getcwd()
    os.chdir(problem_path)
    add_source.add_checker_with_config(problem_config, os.path.join(cur_dir, checker_path))
    os.chdir(cur_dir)

def copy_resource(problem_config, problem_path, resources_path):
    copy_something(problem_config, problem_path, '', resources_path, None)

def copy_solution(problem_config, problem_path, solution_path, tag):
    cur_dir = os.getcwd()
    os.chdir(problem_path)
    add_source.add_solution_with_config(problem_config, os.path.join(cur_dir, solution_path),
                                        polygon2please_verdicts[tag][0], #expected values
                                        polygon2please_verdicts[tag][1]) #possible values
    if tag == 'main':
        add_source.add_main_solution_with_config(problem_config, os.path.join(cur_dir, solution_path))
    os.chdir(cur_dir)

def copy_source(problem_config, problem_path, sources_path):
    copy_something(problem_config, problem_path, '', sources_path, None)
