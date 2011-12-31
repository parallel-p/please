#!/usr/bin/env python3
class EjudgeFormatter:
    def __init__(self):
        pass
    def put_all():
        raise NotImplementedError
        
class NewEjudgeFormatter(EjudgeFormatter):
    def __init__(self, dictionary):
        self.__dictionary = dictionary

    def put_all(self):
        target_path_to_problems = os.path.join('..', 'problems')
        if not os.path.exists(target_path_to_problems):
            os.mkdir(target_path_to_problems)

        names_of_problems = os.listdir('.') 
        for name_of_problem in names_of_problems:                     
            path_to_problem = os.join('.', name_of_problem)
            if not os.path.isdir(path_to_problem)
                continue
            target_path_to_problem = os.join(target_path_to_problems, self.__dictionary[name_of_problem])
            if os.path.exists(target_path_to_problem):
                # make backup!
                shutil.rmtree(target_path_to_problem)
            os.mkdir(target_path_to_problem)
            put_tests(path_to_problem, target_path_to_problem)
            put_checker(path_to_problem, target_path_to_problem)
                        

    def put_tests(self, path_to_problem, target_path_to_problem):
        os.mkdir(io.path.join(target_path_to_problem, 'tests'))
        assert (os.path.isdir(io.path.join(path_to_problem, '.tests'))):
        shutil.copytree(io.path.join(path_to_problem, '.tests'), io.path.join(target_path_to_problem, 'tests'))        
    
    def put_checker(self, path_to_problem, target_path_to_problem):
        pass
    
