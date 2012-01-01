from . import test_info
import tempfile
from ..executors import runner, compiler
from ..diff_test_finder.diff_test_finder import DiffTestFinder
from ..directory_diff import snapshot
import os

class CmdOrGenTestInfo(test_info.TestInfo):
    def __init__(self, executor, args, tags={}):
        """examples: command = "echo", args = ["1", "2", "3"]
        command = "generator.cpp", args = ["17", "42", "100500"]
        """
        self.__executor = executor
        self.__args = args
        super(CmdOrGenTestInfo, self).__init__(tags)
        
    def tests(self):
        problem_dir = os.getcwd() #really?
        
        stdout = tempfile.NamedTemporaryFile(delete = False)
        compiler.compile(self.__executor)

        snapshot_before = snapshot.Snapshot(problem_dir)
        runner.run(self.__executor, self.__args, stdout_fh = stdout)       
        snapshot_after = snapshot.Snapshot(problem_dir, files_to_ignore = [stdout.name])
        
        diff = snapshot.get_changes(snapshot_before, snapshot_after)
        
        exe_dir = os.getcwd() #really?
        mask = self.get_tags().get('mask')
        exclude = self.get_tags().get('exclude')
        diff_test_finder = DiffTestFinder(exe_dir, mask, exclude)
        tests = diff_test_finder.tests(diff, stdout.name)
        
        return tests
    
    def to_please_format(self):
        return self.get_to_please_format_prefix() + self.__executor + " " + " ".join(self.__args)