from . import test_info
import tempfile
from ..executors import runner, compiler

class CmdOrStdGenTestInfo(test_info.TestInfo):
    def __init__(self, executor, args, tags={}):
        """examples: command = "echo", args = ["1", "2", "3"]
        command = "generator.cpp", args = ["17", "42", "100500"]
        """
        super(CmdOrStdGenTestInfo, self).__init__(tags)
        self.__executor = executor
        self.__args = args
        
    def tests(self):
        temp = tempfile.NamedTemporaryFile(delete = False)
        compiler.compile(self.__executor)
        runner.run(self.__executor, self.__args, stdout_fh = temp)
        return [ temp.name ]
    
    def to_please_format(self):
        return self.get_to_please_format_prefix() + self.__executor + " " + " ".join(self.__args)