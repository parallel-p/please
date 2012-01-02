from .. import globalconfig
from ..archiver.ziparchiver import ZIPArchiver
from ..ssh_tools.connector import Connector
from .generic_exporter import GenericExporter
from ..package import config
import shutil
import os

class EjudgeExporter(GenericExporter):
    def __init__(self,network = {},libs = [],problems = []):
        self.connector = Connector(network['host'],network['port'],network['login'],network['password'])
        self.archiver = ZIPArchiver()
        self.problems = problems
        self.libs = libs
        super(EjudgeExporter,self).__init__(self.archiver,self.connector,libs,problems)
    def set_problems(self, problems):
        self.problems = problems
    def get_script(self):
        return globalconfig.export_scripts['ejudge']
    def run_script(self):
        self.connector.run_command('sh '.join(network['destination'],'/',globalconfig.export_scripts['ejudge']['run']))
    def create_archive(self):
        for problem in self.problems:
            with open(problem.join(os.path.sep, 'default.package'), 'r') as configfile:
                conf = config.Config(configfile)
            config.create_simple_config(open(problem.join(os.path.sep, 'default.simple'), 'r'), conf)
        for need_src in globalconfig.export_scripts['ejudge']['scripts']:
            shutil.copy(need_src, os.path.split(need_src)[-1])
        super(EjudgeExporter,self).create_archive()
        self.archiver.add(get_script)
    def upload_file(self):
        self.connector.upload_file(self.archiver.path,network['destination'])
        self.archiver.unzip()
        run_script() 
