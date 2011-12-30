from . import test_info
import tempfile
from ..executors import runner

class CommandTestInfo(test_info.TestInfo):
    def __init__(self, command, args, tags={}):
        """example: command = ["echo"], args = ["1", "2", "3"]"""
        super(CommandTestInfo, self).__init__(tags)
        self.__command = command
        self.__args = args
        
    def tests(self):
        temp = tempfile.NamedTemporaryFile(delete = False)
        f = open(temp.name, 'w')
        runner.run(self.__command[0], self.__args, stdout_fh = f, shell = True)
        return [ temp.name ]
    
    def to_please_format(self):
        return self.get_to_please_format_prefix() + self.__command + " " + " ".join(self.__args)