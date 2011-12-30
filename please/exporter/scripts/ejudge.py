#!/usr/bin/env python3
import configparser, os, io

class EjudgeContest:
    ''' Ejudge contests handling '''
    def __init__(self, config_path):
        self.__static = ""
        self.__abstract_name = ""
        self.__problems_raw = []
        self.__problems = []
        self.__problems_set = set()
        self.__max_problem_id = 1
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
            for param in problem_config['problem']:
                if problem_config['problem'][param] and problem_config['problem'][param][0] == '"' and problem_config['problem'][param][-1] == '"':
                    problem_config['problem'][param] = problem_config['problem'][param][1:-1]
            ej_problem = EjudgeProblem(problem_config['problem'], problem)
            self.__problems.append(ej_problem)
            if ej_problem.abstract:
                self.__abstract_name = ej_problem.short_name
            self.__problems_set.add(ej_problem.internal_name)
            self.__max_problem_id = max(self.__max_problem_id, ej_problem.id)

    def get_backup_list(self):
        return self.__backup_list

    def add_problems(self, problems):
        ''' Adds problems to contest '''
        for problem in problems:
            if problem.internal_name in self.__problems_set:
                self.__backup_list.append(problem.short_name)

        for problem in problems:
            problem.super = self.__abstract_name
            added = False
            for old_problem in self.__problems:
                if old_problem.internal_name == problem.internal_name:
                    added = True
                    old_problem = problem
            if not added:
                self.__problems.append(problem)

    def __str__(self):
        ''' Returns serialized (serv.cfg) string to write to file '''
        res = self.__static + "\n"
        for problem in self.__problems:
            res += str(problem) + "\n"

        return res

class EjudgeProblem:
    def __init__(self, config = [], raw_config = ""):
        ''' Initializes problem using dictionary containing keys from [problem] section of config '''
        self.abstract = "abstract" in config
        self.short_name = "short_name" in config and config["short_name"]
        self.long_name = "long_name" in config and config["long_name"]
        self.internal_name = "internal_name" in config and config["internal_name"]
        self.super = "super" in config and config["super"]
        self.tl = "time_limit" in config and int(config["time_limit"])
        self.ml = "max_vm_size" in config and config["max_vm_size"]
        self.checker = "check_cmd" in config and config["check_cmd"]
        self.id = "id" in config and int(config["id"])
        if "use_stdin" in config:
            self.input = "stdin"
        else:
            self.input = "input" in config and config["input"]
        if "use_stdout" in config:
            self.output = "stdout"
        else:
            self.output = "output" in config and config["output"]

        self.__raw = ''
        for line in raw_config.split('\n'):
            #print(line)
            raw = True
            for x in ['[problem]', 'abstract', 'input', 'output', 'use_stdin', 'use_stdout',
                      'super', 'short_name', 'long_name', 'internal_name', 'time_limit',
                      'max_vm_size', 'check_cmd', 'id', 'test_sfx', 'corr_sfx']:
                if line.startswith(x):
                    raw = False
                    break
            if raw:
                self.__raw += "%s\n" % line

    def __str__(self):
        ''' Returns serialized ([problem] section) problem '''
        res = ""
        res += "[problem]\n"
        if self.abstract:
            res += 'abstract\n'
        if self.id:
            res += 'id = %d\n' % self.id
        if self.super:
            res += 'super = "%s"\n' % self.super
        if self.short_name:
            res += 'short_name = "%s"\n' % self.short_name
        if self.long_name:
            res += 'long_name = "%s"\n' % self.long_name
        if self.internal_name:
            res += 'internal_name = "%s"\n' % self.internal_name
        if self.input:
            if self.input == "stdin":
                res += "use_stdin\n"
            else:
                res += 'input = "%s"\n' % self.input
        if self.output:
            if self.output == "stdout":
                res += "use_stdout\n"
            else:
                res += 'output = "%s"\n' % self.output
        if self.tl:
            res += 'time_limit = %d\n' % round(self.tl)
        if self.ml:
            res += 'max_vm_size = %s\n' % self.ml
        if self.checker:
            res += 'check_cmd = "%s"\n' % self.checker

        res += 'test_sfx = ""\n'
        res += 'corr_sfx = ".a"\n'

        res += self.__raw
        return res

if __name__ == "__main__":
    #print("Exporting to ejudge")
    contest = EjudgeContest("../conf/serve.cfg")
    new_problems = []
    for problem in os.listdir("."):
        if os.path.isdir(problem):
            #print("Adding problem: %s" % problem)
            if os.path.exists(os.path.join(problem, 'default.simple')):
                problem_config = "".join(open(os.path.join(problem, 'default.simple'), 'r').readlines()).split('\n')
                new_problem = EjudgeProblem()
                new_problem.short_name = problem_config[0]
                new_problem.long_name = problem_config[1]
                new_problem.internal_name = new_problem.short_name
                new_problem.input = problem_config[2]
                new_problem.output = problem_config[3]
                new_problem.tl = int(problem_config[4])
                new_problem.ml = problem_config[4] + 'M'
                new_problem.checker = problem_config[5]

                new_problems.append(new_problem)
    contest.add_problems(new_problems)
    print(str(contest))
