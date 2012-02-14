from .. import globalconfig
from .generic_exporter import GenericExporter
from ..package import config
from ..template.template_utils import get_template_full_path
from ..solution_tester.package_config import PackageConfig
import shutil
import os
class ShareConnector:
    def __init__(self, destination):
        self.destination = destination
    def upload_file(self,src,dst):
        (shutil.copy2 if os.path.isfile(src) else shutil.copytree)(src,self.host)
    def download_file(self,src,dst):
        (shutil.copy2 if os.path.isfile(src) else shutil.copytree)(src,self.host)
    
class PCMS2Exporter(GenericExporter):
    def __init__(self,network = {},libs = [],problems = []):
        self.connector = ShareConnector(network['host'])
        self.network = network
        self.problems = problems
        self.libs = libs
        super(PCMS2Exporter,self).__init__(None,self.connector,libs,problems)
    def create_archive(self):
        pass
    def set_problems(self, problems):
        self.problems = problems
    def set_contest_id(self, contest_id):
        self.contest_id = contest_id.replace('.', os.path.sep)
    def run_script(self):
        for problem in self.problems:
            conf = PackageConfig.get_config(problem)
            replaces = {
                '$$please-version$$'              : str(globalconfig.please_version),
                '$$id$$'                          : self.contest_id.replace(os.path.sep,'.'),
                '$$test-count$$'                  : str(len(os.listdir(os.path.join(problem,'.tests'))) // 2),
                '$$input$$'                       : conf['input'],
                '$$output$$'                      : conf['output'],
                '$$time-limit$$'                  : str(int(conf['time_limit'])),
                '$$memory-limit$$'                : str(int(float(conf['memory_limit'])*1024*1024)),
                '$$checker-without-extention$$'   : conf['checker'].split('.')[0]
            }
            with open(os.path.join(globalconfig.root, globalconfig.export_scripts['pcms2']['problem_template']), 'r') as template_src_file:
                template_src = list(map(lambda x : x.rstrip(), template_src_file.readlines()))
                for ind in range(len(template_src)):
                    for replace in replaces:
                        template_src[ind] = template_src[ind].replace(replace, replaces[replace])
            with open(os.path.join(self.network['host'],self.contest_id,problem,'problem.xml'), 'w') as new_src:
                new_src.write('\r\n'.join(template_src))
    def upload_file(self):
        plpt = os.path.join(self.network['host'],self.contest_id)
        for problem in self.problems:
            if os.path.exists(os.path.join(plpt, problem, 'tests')):
                shutil.rmtree(os.path.join(plpt, problem, 'tests'))
            #copy_with_leading_zeroes = lambda src,dst : shutil.copy2(src, 
            #                                                  os.path.join(
            #                                                      os.path.split(src)[0], 
            #                                                      os.path.split(src)[1].split('.')[0].zfill(2), 
            #                                                      os.path.split(src)[1].split('.')[1] 
            #                                                      if len(os.path.split(src)[1].split('.')) > 1 else None))
            shutil.copytree(src = os.path.join(problem,'.tests'), dst = os.path.join(plpt,problem, 'tests'))
            for filename in os.listdir(os.path.join(plpt,problem, 'tests')):
                if '.a' in filename:
                    os.rename(os.path.join(os.path.join(plpt,problem, 'tests', filename)), 
                            os.path.join(os.path.join(plpt,problem, 'tests', filename.zfill(4))))
                else:
                    os.rename(os.path.join(os.path.join(plpt,problem, 'tests', filename)), 
                            os.path.join(os.path.join(plpt,problem, 'tests', filename.zfill(2))))
            conf = PackageConfig.get_config(problem)
            #self.archiver.add(conf['checker'], os.path.join(problem, os.path.split(conf['checker'])[-1]))
            checker_name = os.path.split(conf['checker'])[1]
            if os.path.exists(os.path.join(plpt, problem, checker_name)):
                shutil.unlink(os.path.join(plpt, problem, checker_name))
            shutil.copy2(src = os.path.join(problem, checker_name), dst = os.path.join(plpt,problem))