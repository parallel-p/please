from os.path import exists
import os.path
from shutil import copy
from .. import globalconfig

def get_template_full_path(template_name):
    default_template_path = os.path.join(globalconfig.root, globalconfig.default_template_dir, template_name)
    user_template_path = os.path.join(globalconfig.user_template_dir, template_name)
    if (globalconfig.user_template_dir != "") and exists(user_template_path):
        return user_template_path
    elif exists(default_template_path):
        return default_template_path
    else:
        return None
    
def copy_or_create(source_path, destination_path):
    ''' If source exists copies it, otherwise creates empty file '''
    try:
        if (source_path != None) and (exists(source_path)):
            copy(source_path, destination_path)
        else:
            open(destination_path, 'w').close()
    except:
        if source_path is not None:
            source = source_path
        else:
            source = "<none>"
        print("Warning: Cannot copy " + source + " to " + destination_path + "\n")
        return False
    return True

def make_statement_name(human_language, file_name):
    ''' Example: make_file_name(rus, test) => "test.rus.tex" '''
    if human_language != "":
        return file_name + "." + human_language + ".tex"
    else:
        return file_name + ".tex"
