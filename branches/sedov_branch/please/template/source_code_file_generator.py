from .template_utils import get_template_full_path
from .template_utils import copy_or_create
import os.path

def generate_source_file(path, programming_language, name):    
    ''' ("path/", "cpp", "validator") => path/validator.cpp will be created, returns name (validator.cpp) or False '''    
    
    file_name = name + "." + programming_language
    path_from = get_template_full_path(file_name)
    path_to = os.path.join(path, file_name)
    return copy_or_create(path_from, path_to) and file_name

    
def generate_validator(path = ".", programming_language = "cpp"): 
    return generate_source_file(path, programming_language, "validator")
    
    
def generate_checker(path = ".", programming_language = "cpp"): 
    return generate_source_file(path, programming_language, "checker")
    
def generate_solution(path = ".", programming_language = "cpp"): 
    return generate_source_file(path, programming_language, "solution")
    
    

    
    
    
