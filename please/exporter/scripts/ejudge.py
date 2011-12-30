#!/usr/bin/env python3
import configparser, os, io

class EjudgeContest:
    ''' Ejudge contests handling '''
    def __init__(self, config_path):
        self.__static = ""
        self.__problems_raw = []
        self.__problems = []
        config = open(config_path, 'r')
        in_problem = False
        for line in config.readlines():
            if line[:-1] == '[problem]':
                self.__problems_raw.append("[problem]\n")
                in_problem = True
            elif line[0] == '[':
                in_problem = False
            elif in_problem:
                self.__problems_raw[-1] += line
            if not in_problem:
                self.__static += line

        for problem in self.__problems_raw:
            problem_config = configparser.RawConfigParser(allow_no_value = True)
            problem_config.read_string(problem)
            self.__problems.append(EjudgeProblem(problem_config['problem']))

    def add_problems(self, problems):
        ''' Adds problems to contest, backups equal'''
        pass

    def __str__(self):
        ''' Returns serialized (serv.cfg) string to write to file '''
        res = ""
        for problem in self.__problems:
            res += "[problem]\n"
            if problem.abstract:
                res += "abstract\n"
            if problem.short_name:
                res += "short_name = %s\n" % problem.short_name
        return res

class EjudgeProblem:
    def __init__(self, config):
        ''' Initializes problem using dictionary containing keys from [problem] section of config '''
        self.abstract = "abstract" in config
        self.short_name = config["short_name"] or None
        pass
    def __str__(self):
        ''' Returns serialized ([problem] section) problem '''
        pass

if __name__ == "__main__":
    print("Exporting to ejudge")
    contest = EjudgeContest("../conf/serve.cfg")
    print(str(contest))
    for problem in os.listdir("."):
        print("Adding problem: %s" % problem)
