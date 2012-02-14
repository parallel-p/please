import os

from ..command_line.generate_tests import generate_tests
from ..solution_tester.package_config import PackageConfig

class GenericExporter:
    def __init__(self,archiver = None, connector = None,libs = [],problems = []):
        self.archiver = archiver
        self.problems = problems
        self.connector = connector
    def create_archive(self):
        for problem in self.problems:
            os.chdir(problem)
            generate_tests()
            conf = PackageConfig.get_config()
            # TODO: check if conf is None
            #with open('default.package', 'r') as f:
            #    conf = Config(f.read())
            if self.archiver:
                self.archiver.add(conf['checker'], os.path.join(problem, os.path.split(conf['checker'])[-1]))
            #if not os.path.exists(conf['checker']):
            #    print(conf['checker'])
            #    print(-1/0)
            os.chdir('..')
            self.archiver.add_folder(problem, conf['shortname'])
    
  
        
        
        
