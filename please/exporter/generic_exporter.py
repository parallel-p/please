import shutil
import os
from ..archiver import Archiver
from ..ssh_tools.connector import Connector
from ..build_all.build_tools import build_all
class GenericExporter:
    def __init__(self,archiver = None, connector = None,libs = [],problems = []):
        self.archiver = archiver
        self.problem_list = problem_list
        self.need_testlib = need_testlib
        self.connector = connector
    def create_archive(self):
        for problem in problems:
            os.chdir(problem)
            build_all()
            os.chdir('..')
            archiver.add(problem)
    def upload(self):
        connector.upload_file(self.archiver.path)
    
  
        
        
        