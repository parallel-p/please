import shutil
import os
from ..archiver import Archiver
from ..ssh_tools.connector import Connector
from generic_exporter import GenericExporter
class EjudgeExporter(GenericExporter):
    def __init__(self,network = {},libs = [],problems = []):
        self.connector = Connector(network['host'],network['port'],network['login'],network['password'])
        self.archiver = ZIPArchiver()
        super(EjudgeExporter,self).__init__(self.archiver,self.connector,libs,problems)
    def get_script():
        pass
    def run_script():
        pass
    def create_archive():
        super(EjudgeExporter,self).create_archive()
        self.archiver.add(get_script)
    def upload_file():
        self.connector.upload_file(self.archiver.path,network['destination'])
        run_script()
        
        
        
    
  
        