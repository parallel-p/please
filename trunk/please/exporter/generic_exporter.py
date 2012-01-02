import shutil
import os
from ..command_line.generate_tests import generate_tests
from ..ssh_tools.connector import Connector
from ..build_all.build_tools import build_all
class GenericExporter:
    def __init__(self,archiver = None, connector = None,libs = [],problems = []):
        self.archiver = archiver
        self.problems = problems
        self.connector = connector
    def create_archive(self):
        for problem in self.problems:
            os.chdir(problem)
            generate_tests()
            os.chdir('..')
            self.archiver.add_folder(problem, problem)
    
  
        
        
        