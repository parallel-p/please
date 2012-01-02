import shutil
import os
from ..package.config import Config
from ..command_line.generate_tests import generate_tests
from ..ssh_tools.connector import Connector
from ..build_all.build_tools import build_all
from please.checkers.standard_checkers_utils import add_standard_checker_to_solution

class GenericExporter:
    def __init__(self,archiver = None, connector = None,libs = [],problems = []):
        self.archiver = archiver
        self.problems = problems
        self.connector = connector
    def create_archive(self):
        for problem in self.problems:
            os.chdir(problem)
            generate_tests()
            with open('default.packahe', 'r') as f:
                conf = Config(f.read())
            if not os.path.exists(conf['checker']):
                add_standart_checker_to_solution(conf['checker'])
            os.chdir('..')
            self.archiver.add_folder(problem, problem)
    
  
        
        
        
