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
            with open('default.package', 'r') as f:
                conf = Config(f.read())
            self.archiver.add(conf['checker'], os.path.join(problem, os.path.split(conf['checker'])[-1]))
            #if not os.path.exists(conf['checker']):
            #    print(conf['checker'])
            #    print(-1/0)
            os.chdir('..')
            self.archiver.add_folder(problem, problem)
    
  
        
        
        
