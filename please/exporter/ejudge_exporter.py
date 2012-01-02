from .. import globalconfig
from ..archiver.ziparchiver import ZIPArchiver
from ..ssh_tools.connector import Connector
from .generic_exporter import GenericExporter
from ..package import config
from ..template.template_utils import get_template_full_path
import shutil
import os

class EjudgeExporter(GenericExporter):
    def __init__(self,network = {},libs = [],problems = []):
        self.connector = Connector(network['host'],network['port'],network['login'],network['password'])
        self.network = network
        self.archiver = ZIPArchiver('please.archive.zip')
        self.problems = problems
        self.libs = libs
        super(EjudgeExporter,self).__init__(self.archiver,self.connector,libs,problems)
    def set_problems(self, problems):
        self.problems = problems
    def set_contest_id(self, contest_id):
        self.contest_id = contest_id
    def get_script(self):
        return globalconfig.export_scripts['ejudge']
    def run_script(self):
        self.connector.run_command('cd '+ self.network['destination'] + '/' + self.contest_id + '/please_tmp/ ; '+ '/usr/bin/env python3 ' + self.network['destination'] + '/' + self.contest_id + '/please_tmp/' + globalconfig.export_scripts['ejudge']['run'])
    def create_archive(self):
        for problem in self.problems:
            with open(problem + os.path.sep + 'default.package', 'r') as configfile:
                conf = config.Config(configfile.read())
            config.create_simple_config(problem + os.path.sep + 'default.simple', conf)
        for need_src in globalconfig.export_scripts['ejudge']['scripts']:
            self.archiver.add(globalconfig.root + os.path.sep + need_src, os.path.split(need_src)[-1])
        super(EjudgeExporter,self).create_archive()
        self.archiver.close()
        #self.archiver.add(self.get_script())
    def upload_file(self):
        plpt = self.network['destination']+'/'+self.contest_id+'/'
        #self.connector.run_command('rm -rf ' + plpt + 'please_tmp; mkdir ' + plpt)
        self.connector.upload_file(self.archiver.path, plpt+'/'+os.path.split(self.archiver.path)[-1])
        self.run_script() 
