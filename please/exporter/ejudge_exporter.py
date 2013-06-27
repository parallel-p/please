import os

from .. import globalconfig
from ..archiver.ziparchiver import ZIPArchiver
from ..ssh_tools.connector import Connector
from .generic_exporter import GenericExporter
from ..package import config
from ..package.package_config import PackageConfig

class EjudgeExporter(GenericExporter):
    def __init__(self,network = {},libs = [],problems = []):
        self.connector = Connector(network['host'], network['port'], network['login'], network.get('password'), network.get('private_key'))
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
      self.connector.run_command('cd {}; /usr/bin/env python3.2 {}'.format(os.path.join(self.network['destination'], self.contest_id, 'please_tmp'),
os.path.join(self.network['destination'], self.contest_id , 'please_tmp', globalconfig.export_scripts['ejudge']['run'])).replace('\\', '/'))

    def create_archive(self):
        for problem in self.problems:
            conf = PackageConfig.get_config(dir = problem)
            # TODO: check if conf is None
            #with open(problem + os.path.sep + 'default.package', 'r') as configfile:
            #    conf = config.Config(configfile.read())
            config.create_simple_config(os.path.join(problem, 'default.simple'), conf)
        for need_src in globalconfig.export_scripts['ejudge']['scripts']:
            self.archiver.add(os.path.join(globalconfig.root, need_src), os.path.split(need_src)[-1])
        super(EjudgeExporter,self).create_archive()
        self.archiver.close()
        #self.archiver.add(self.get_script())
    def upload_file(self):
        plpt = os.path.join(self.network['destination'], self.contest_id)
        # self.connector.run_command('rm -rf ' + plpt + 'please_tmp; mkdir ' + plpt + 'please_tmp')
        self.connector.upload_file(self.archiver.path, os.path.join(plpt, os.path.split(self.archiver.path)[-1]).replace('\\', '/'))

