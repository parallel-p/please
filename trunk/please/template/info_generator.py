import os
import time
import hashlib


def create_time_file(root_path):
    """
    Description:
    This function creates in root folder new system folder (.please),
    that contains a file(time.config), that contains it's creation time 
    """
    system_folder_path = os.path.join(root_path, ".please")
    os.mkdir(system_folder_path)
    time_file_path = os.path.join(system_folder_path, "time.config")
    
    with open(time_file_path, "w", encoding = 'UTF8') as time_file:
        time_sec = str(time.time())
        time_file.write(time_sec)

def create_md5_file(root_path):
    '''
    Creates md5conf.py with md5-sums of initial files
    '''
    with open(os.path.join(root_path, '.please', 'md5.config'), 'w') as md5file:
        d = dict(checker='checker.cpp', 
                   validator='validator.cpp', 
                   statement=os.path.join('statements', 'default.ru.tex'),
                   description=os.path.join('statements', 'description.ru.tex'),
                   analysis=os.path.join('statements', 'analysis.ru.tex'),
                   tests_description='tests.please',
                   main_solution=os.path.join('solutions', 'solution.cpp')
                  )
        for (resource, dest) in d.items():
            filepath = os.path.join(root_path, dest) 
            if os.path.exists(filepath):
                m = hashlib.md5()
                with open(filepath,'r+b') as cur_file:
                    m.update(cur_file.read())
                md5file.write(resource + ":" + m.hexdigest() + "\n")

