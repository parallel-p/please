#!/usr/bin/env python3
import configparser, os, io

# run_tests.py will run ejudge_formatter test correct only with relative imports
try:
    from . import ejudge_formatter, backupper
except ImportError:
    import please.exporter.scripts.ejudge_formatter as ejudge_formatter
    import please.exporter.scripts.backupper as backupper

class EjudgeContest:
    ''' Ejudge contests handling '''
    def __init__(self, config_path):
        self.__static = ""
        self.__abstract_name = ""
        self.__problems_raw = []
        self.__problems = []
        self.__problems_byname = {}
        self.__max_problem_id = 0
        self.__advanced_layout = False
        with open(config_path, 'r', encoding = "utf-8") as config:
            in_problem = False
            for line in config.readlines():
                if line[:-1] == 'advanced_layout':
                    self.__advanced_layout = True
                if line[:-1] == '[problem]':
                    self.__problems_raw.append("[problem]\n")
                    in_problem = True
                elif line[0] == '[':
                    in_problem = False
                elif in_problem and line != "\n":
                    self.__problems_raw[-1] += line
                if not in_problem:
                    self.__static += line

        for problem in self.__problems_raw:
            problem_config = configparser.RawConfigParser(allow_no_value = True)
            problem_config.read_string(problem)
            ej_problem = EjudgeProblem(problem_config['problem'], problem)
            if ej_problem.abstract:
                self.__abstract_name = ej_problem.short_name
            if ej_problem.internal_name is False:
                ej_problem.internal_name = ej_problem.short_name
            self.__problems_byname[ej_problem.internal_name] = ej_problem
            self.__problems.append(ej_problem)
            self.__max_problem_id = max(self.__max_problem_id, ej_problem.id)

    def get_version(self):
        if not self.__advanced_layout:
            return 0
        else:
            return 1

    def get_matches(self):
        return self.__matching

    def add_problems(self, problems):
        ''' Adds problems to contest '''
        self.__matching = {}
        for problem in problems:
            problem.super = self.__abstract_name
            if problem.internal_name in self.__problems_byname:
                copy_problem(problem, self.__problems_byname[problem.internal_name])
            else:
                self.__max_problem_id += 1
                problem.id = self.__max_problem_id
                self.__problems.append(problem)
            self.__matching[problem.internal_name] = problem.internal_name

    def __str__(self):
        ''' Returns serialized (serv.cfg) string to write to file '''
        res = self.__static + "\n"
        for problem in self.__problems:
            res += str(problem) + "\n"

        return res

class EjudgeProblem:
    def __init__(self, config = [], raw_config = ""):
        ''' Initializes problem using dictionary containing keys from [problem] section of config '''
        self.__config = config
        self.abstract = "abstract" in config
        self.short_name = self.config_param("short_name")
        self.long_name = self.config_param("long_name")
        self.internal_name = self.config_param("internal_name")
        self.super = self.config_param("super")
        self.tl = self.config_param("time_limit")
        if self.tl is not None:
            self.tl = int(self.tl)
        self.ml = self.config_param("max_vm_size")
        self.checker = self.config_param("check_cmd")
        self.id = self.config_param("id")
        if self.id is not None:
            self.id = int(self.id)
        if "use_stdin" in config:
            self.input = '"stdin"'
        else:
            self.input = self.config_param("input_file")
        if "use_stdout" in config:
            self.output = '"stdout"'
        else:
            self.output = self.config_param("output_file")
        self.test_pat = self.config_param("test_pat")
        self.corr_pat = self.config_param("corr_pat")
        self.time_limit_millis = self.config_param("time_limit_millis")
        if self.time_limit_millis is not None:
            self.time_limit_millis = float(self.time_limit_millis) / 1000

        self.__raw = ''
        for line in raw_config.split('\n'):
            raw = True
            for x in ['[problem]', 'abstract', 'input_file', 'output_file', 'use_stdin', 'use_stdout',
                      'super', 'short_name', 'long_name', 'internal_name', 'time_limit',
                      'max_vm_size', 'check_cmd', 'id', 'test_pat', 'corr_pat', 'time_limit_millis']:
                if line.startswith(x):
                    raw = False
                    break
            if raw:
                self.__raw += "%s\n" % line

    def config_param(self, param):
        return param in self.__config and self.__config[param]

    def __str__(self):
        ''' Returns serialized ([problem] section) problem '''
        res = ""
        res += "[problem]\n"
        if self.abstract:
            res += 'abstract\n'
        if self.id:
            res += 'id = %d\n' % self.id
        if self.super:
            res += 'super = %s\n' % self.super
        if self.short_name:
            res += 'short_name = %s\n' % self.short_name
        if self.long_name:
            res += 'long_name = %s\n' % self.long_name
        if self.internal_name:
            res += 'internal_name = %s\n' % self.internal_name
        if self.input:
            if self.input == '"stdin"':
                res += "use_stdin\n"
            else:
                res += 'input_file = %s\n' % self.input
        if self.output:
            if self.output == '"stdout"':
                res += "use_stdout\n"
            else:
                res += 'output_file = %s\n' % self.output
        if self.time_limit_millis:
            res += 'time_limit_millis = %s\n' % int(self.time_limit_millis * 1000)
        elif self.tl:
            res += 'time_limit = %d\n' % round(self.tl)
        if self.ml:
            res += 'max_vm_size = %s\n' % self.ml
        if self.checker:
            res += 'check_cmd = %s\n' % self.checker
        if self.test_pat:
            res += 'test_pat = %s\n' % self.test_pat
        if self.corr_pat:
            res += 'corr_pat = %s\n' % self.corr_pat

        res += self.__raw
        return res

class EjudgeProblemToCopy:
    def __init__(self, problem_from, problem_to, problem_checker):
        """
            from is <internal name> (so all problem lays in ./please_tmp/<from>/)
            to is <short name> where we should copy our problem (for new format: ../problems/<to>/)
            checker is relative path to checker file
        """
        self.problem_from = problem_from
        self.problem_to = problem_to
        self.problem_checker = problem_checker

def without_extension(s):
    return os.path.splitext(s)[0]

def no_quotes(s):
    if s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    else:
        return s

def copy_problem(src, dst):
    """ Copies only modified-by-user values from src to dst problem """
    for x in ["long_name", "input", "output", "time_limit_millis",
              "short_name", "ml", "checker", "test_pat", "corr_pat"]:
        dst.__dict__[x] = src.__dict__[x]

def export(inp, out):
    contest = EjudgeContest(inp)
    new_problems = []
    for problem in os.listdir("."):
        if os.path.isdir(problem):
            if os.path.exists(os.path.join(problem, 'default.simple')):
                with open(os.path.join(problem, 'default.simple'), 'r', encoding = 'utf-8') as simple_config:
                    problem_config = "".join(simple_config.readlines()).split('\n')
                new_problem = EjudgeProblem()
                new_problem.short_name = '"%s"' % problem_config[7]
                new_problem.long_name = '"%s"' % problem_config[1]
                new_problem.internal_name = '"%s"' % problem_config[0]
                new_problem.input = '"%s"' % problem_config[2]
                new_problem.output = '"%s"' % problem_config[3]
                new_problem.time_limit_millis = float(problem_config[4])
                new_problem.ml = str(int(float(problem_config[5]))) + 'M'
                new_problem.checker = '"%s"' % without_extension(problem_config[6])
                new_problem.checker_ext = '%s' % problem_config[6]
                new_problem.test_pat = '"%d"'
                new_problem.corr_pat = '"%d.a"'

                new_problems.append(new_problem)
    contest.add_problems(new_problems)
    to_copy = []
    for problem in new_problems:
        to_copy.append(EjudgeProblemToCopy(no_quotes(problem.internal_name), no_quotes(problem.internal_name), problem.checker_ext))

    if contest.get_version() == 0:
        formatter = ejudge_formatter.OldEjudgeFormatter(to_copy)
    else:
        formatter = ejudge_formatter.NewEjudgeFormatter(to_copy)
    formatter.put_all()

    with open(out, 'w', encoding = 'utf-8') as f:
        f.write(str(contest))

if __name__ == "__main__" and os.path.exists('../conf/serve.cfg'):
    # Backup whole contest before doing something
    backupper.make_backup()
    export('../conf/serve.cfg', '../conf/serve.cfg')
