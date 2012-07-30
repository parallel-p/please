from ..template import problem_template_generator as problem_generator
from ..package import config
import os
import shutil

def list_to_str(data_list):
    return ', '.join(data_list)

def create_stub(short_task_name, time_limit=None, memory_limit=None, file_in=None, file_out=None, tags=None, path=None):
    """
    Creates or rewrites problem stub "path/short_task_name" with given arguments
    """
    
    cwd = os.getcwd()
    os.chdir(path)
    
    try:
        problem_generator.generate_problem(short_task_name, False)
    except problem_generator.ProblemExistsError:
        shutil.rmtree(os.path.join(path, short_task_name))
        problem_generator.generate_problem(short_task_name, False)
    
    with open(os.path.join(short_task_name, 'default.package'), 'r', encoding='utf-8') \
                                                                       as config_file:
        config_data=config_file.read()
        
    problem_config = config.Config(config_data, file=os.path.join(short_task_name, 'default.package'))
    
    if (file_in == ''):
        file_in = 'stdin'
    if (file_out == ''):
        file_out = 'stdout'
    if tags != None:
        tags = list_to_str(tags)
        
    replaces = {'shortname': short_task_name, 'time_limit': time_limit, 'memory_limit': memory_limit,
                'input': file_in, 'output': file_out, 'tags': tags}
    
    for key, value in replaces.items():
        if value == None:
            continue
        problem_config[key] = value
       
    os.chdir(cwd)
    
    return problem_config
    
def commit_config_file(problem_config, problem_path):
    if not problem_path is None:
        cur_dir = os.getcwd()
        os.chdir(problem_path)
    
    with open('default.package', 'w', encoding='utf-8') \
                                                                       as config_file:
        config_file.write(problem_config.get_text())
    
    if not problem_config is None:
        os.chdir(cur_dir)
