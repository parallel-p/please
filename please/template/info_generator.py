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
	
	time_file = open(time_file_path, "w", encoding = 'UTF8')
	time_sec = str(time.time())
	time_file.write(time_sec)
	time_file.close()

def create_md5_file(root_path):
    '''
    Creates md5conf.py with md5-sums of initial files
    '''
    md5file = open(os.path.join(root_path, '.please', 'md5.config'), 'w')
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
            m.update(open(filepath,'r+b').read())
            md5file.write(resource + ":" + m.hexdigest() + "\n")
    md5file.close()