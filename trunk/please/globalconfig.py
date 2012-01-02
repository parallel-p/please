import os
from .exporter.ejudge_exporter import EjudgeExporter
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
    'scripts' : ['ejudge.py', 'ejudge_formatter.py', 'backupper.py'],
    'run' : 'ejudge.py'
  }
}

servers = {
  'zhuravlev_ejudge' : EjudgeExporter(
    network = {
      'host' : '192.168.16.28',
      'port' : '22',
      'login' : 'ejudge',
      'password' : 'ejudge'
    },
    libs = []
  )
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

#information about ejudge server (protocol pscp)
ejudge_host = "192.168.16.37"
ejudge_port = "22"
ejudge_login = "ejudge"
ejudge_password = "ejudge"
ejudge_contests_dir = "/home/judges/"

#information about polygon
access = {'login': 'makhmedov', "password": "lzlzfbr"}
polygon_url = "http://codecenter.sgu.ru:8081/polygon"

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

