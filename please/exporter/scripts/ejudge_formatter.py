#!/usr/bin/env python3
import os, shutil
    
class EjudgeFormatter:
    def __init__(self):
        pass
    def put_all():
        raise NotImplementedError
        
class NewEjudgeFormatter(EjudgeFormatter):
    def __init__(self, problems):
        # problems is a list of structures:
        # it has three parameters:
        # 1) problem_from - the shortname of this problem
        # 2) problem_to - the target shortname in the Ejudge of this problem
        # 3) problem_checker - the name of checker.
        self.__problems = problems

    def __put_tests(self, path_to_problem, target_path_to_problem):
        if not os.path.isdir(os.path.join(path_to_problem, '.tests')):
            os.mkdir(os.path.join(path_to_problem, '.tests'))
        shutil.copytree(os.path.join(path_to_problem, '.tests'), os.path.join(target_path_to_problem, 'tests'))        

    def __put_checker(self, path_to_problem, target_path_to_problem, name_of_checker):
        if os.path.splitext(name_of_checker)[1] in ['.cpp', '.c', '.c++', '.cxx']:
            checker = ""
            with open(os.path.join(path_to_problem, name_of_checker)) as f:
                checker = f.read()
            checker = "#define EJUDGE\n" + checker
            with open(os.path.join(target_path_to_problem, name_of_checker), 'w', encoding = 'utf-8') as f:
                f.write(checker)
        else:
            shutil.copyfile(os.path.join(path_to_problem, name_of_checker), os.path.join(target_path_to_problem, name_of_checker))

    def put_all(self):
        target_path_to_problems = os.path.join('..', 'problems')
        if not os.path.exists(target_path_to_problems):
            os.mkdir(target_path_to_problems)

        for problem in self.__problems:                     
            path_to_problem = os.path.join('.', problem.problem_from)
            if not os.path.isdir(path_to_problem):
                print(path_to_problem)
                raise FileNotFoundException
                
            target_path_to_problem = os.path.join(target_path_to_problems, problem.problem_to)
            if os.path.exists(target_path_to_problem):
                shutil.rmtree(target_path_to_problem)
            os.mkdir(target_path_to_problem)
            self.__put_tests(path_to_problem, target_path_to_problem)
            self.__put_checker(path_to_problem, target_path_to_problem, problem.problem_checker)
                        

class OldEjudgeFormatter(EjudgeFormatter):
    def __init__(self):
        raise NotImplementedError
    def put_all(self):
        raise NotImplementedError

'''
class MyProblem:
    def __init__(self, problem_from, problem_to, problem_checker):
        self.problem_from = problem_from
        self.problem_to = problem_to
        self.problem_checker = problem_checker

NEF = NewEjudgeFormatter([MyProblem('a', 'abacaba', 'checkernew.cpp')])
NEF.put_all()
'''
