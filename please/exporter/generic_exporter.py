from ..archiver import Archiver
class GenericExporter:
    def __init__(self,archiver = None,need_testlib = True,network_settings = {},problem_list, arglist = {}):
        self.archiver = archiver
        self.network_settings = network_settings
        self.problem_list = problem_list
        self.need_testlib = need_testlib
        
    def create_archive(self):
        for problem in problem_list:
            archiver.add(problem)
    def upload(self):
        path = archiver.path
        if network_settings['type'] == 'ssh':
            pass 
        elif network_settings['type'] == 'share':
            pass
        else:
            raise Exception('Unknown connection type: ' + network_settings['type'])
        
        
        
        
        