import os
import time
from .invoker.invoker import ExecutionLimits
from logging import INFO,ERROR,CRITICAL,WARNING,DEBUG
please_version = 0.2
root = os.path.split(__file__)[0]

default_limits = ExecutionLimits(20, 3512)
stress_up = 1000000
# templates
default_template_dir = "templates"
default_template_contest = "contest.tex"
default_template_statement = "statement.tex"
default_template_analysis = "analysis.tex"
default_package = "default.package"
default_tests_config = "tests.please"
user_template_dir = ""

default_programming_language = "cpp"
default_human_language = "ru"

export_scripts = {
  'ejudge' : {
    'scripts' : [os.path.join('exporter','scripts',filename) for filename in ['ejudge.py', 'ejudge_formatter.py', 'backupper.py']],
    'run' : 'ejudge.py'
  }
}


# config for folders in problem
statements_dir = "statements"
solutions_dir = "solutions"
tests_dir = "tests"

# temporary folders
temp_statements_dir = ".statements"
temp_tests_dir = ".tests"

# logging conts
standart_logging_lvl = INFO
detailed_logging_lvl = DEBUG
console_logging_lvl = INFO

checkers_dir = "checkers"
logs = ["detailed.log", "please.log"]

# checker return codes -> verdicts
checker_return_codes = {0:"OK", 1:"WA", 2:"PE"}

#temporary solution output file
temp_solution_out_file = ".out"

#information about polygon
access = {'login': 'makhmedov', "password": "lzlzfbr"}
polygon_url = "http://codecenter.sgu.ru:8081/polygon"
polygon_url = 'http://178.217.103.1:8090/polygon'
access = {'login': 'tigvarts_oivanov', "password": "51234"}

#information about problems' svn-repository
#set 'url' to '' (empty string) if you don't want to work with svn,
#but do not delete neither this dictionary, nor any key in it!
#type: personal (you control your repository) / public
svn = {     'type': '', #personal',
             'url': '', #https://please-svn.googlecode.com/svn/problems/',
        'username': '', #gurovic@gmail.com', 
        'password': ''}#ez9NP2Hz5BD5'}

#exports = {
#    'lksh': export.Ejudge('ssh://ejudge@ejudge.lksh.ru'),
#    'spbsu': export.Testsys('/mnt/server/D/problems/'),
#}

# Default latex template vars: used for generating one problem
default_template_vars = {
    "name": "Contest name",
    "location": "",
    "date": time.strftime("%A, %d %B")
}
