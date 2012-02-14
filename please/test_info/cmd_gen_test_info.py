from . import test_info
from . import test_file_sort
import tempfile
from ..executors import runner, compiler
from ..diff_test_finder.diff_test_finder import DiffTestFinder
from ..directory_diff.snapshot import Snapshot
from ..utils.form_error_output import process_err_exit
import os
from ..utils.exceptions import PleaseException

class CmdOrGenTestInfo(test_info.TestInfo):
    def __init__(self, executor, args, tags={}, comment=''):
        """
        Example:
            executor = "generator.cpp", args = ["17", "42", "100500"]
        """
        self.__executor = executor
        self.__args = args
        super(CmdOrGenTestInfo, self).__init__(tags, comment)
    
    def __eq__(self, other):
        return self.__executor == other.__executor and self.__args == other.__args
        
    def tests(self):
        problem_dir = os.getcwd() #really?
        
        stdout = tempfile.NamedTemporaryFile(delete = False)
        compiler.compile(self.__executor)

        snapshot_before = Snapshot(problem_dir)
        invoker_result, retstdout, reterror = runner.run(
                self.__executor, self.__args, stdout = stdout)
        if invoker_result.verdict != "OK":
            raise PleaseException(
                process_err_exit("Generator %s with args %s crashed with"
                    % (self.__executor, " ".join(self.__args)),
                    invoker_result.verdict, invoker_result.return_code,
                    retstdout, reterror))
        snapshot_after = Snapshot(problem_dir, files_to_ignore = [stdout.name])
        
        diff = snapshot_before.get_changes(snapshot_after)
        
        exe_dir = os.getcwd() #really?
        mask = self.get_tags().get('mask')
        exclude = self.get_tags().get('exclude')
        diff_test_finder = DiffTestFinder(exe_dir, mask, exclude)
        tests = diff_test_finder.tests(diff, stdout.name)
        desc = diff_test_finder.get_desc()
        
        zipped = list(zip(tests, desc))
        zipped.sort(key = lambda x : test_file_sort.sorting_key(x[0]))
        tests, desc = zip(*zipped)
        self.set_desc(desc)        

        #remove trash
        for file in diff[1]:
            if os.path.relpath(file, exe_dir) not in tests:
                os.remove(os.path.join(exe_dir, file))
        return tests
    
    def to_please_format(self):
        return ' '.join([self.get_prefix(), self.__executor, ' '.join(self.__args), self.get_suffix()]).strip()
