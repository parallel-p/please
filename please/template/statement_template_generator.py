from .template_utils import *
    
def __generate_file(path, human_language, name, template):
    ''' Copies (or creates if not exists) path/name{.language}.tex  from templates_dir/template '''
    template_path = get_template_full_path(template)
    file_name = make_statement_name(human_language, name)
    new_path = path + "/" + file_name
    return copy_or_create(template_path, new_path) and file_name

def generate_statement(path = ".", human_language = "", name = "default"):
    ''' Returns name (without path) of created file '''
    return __generate_file(path, human_language, name, "default.tex")
    
def generate_analysis(path = ".", human_language = "", name = "analysis"):
    ''' Returns name (without path) of created file '''
    return __generate_file(path, human_language, name, "analysis.tex")
    
def generate_description(path = ".", human_language = "", name = "description"):
    ''' Returns name (without path) of created file '''    
    return __generate_file(path, human_language, name, "description.tex")