from . import test_info
from . import test_file_sort
import tempfile
from ..executors import runner, compiler
from .. import lang_config
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
        mask = tags.get('mask')
        exclude = tags.get('exclude')
        self.diff_test_finder = DiffTestFinder(mask, exclude)
        super(CmdOrGenTestInfo, self).__init__(tags, comment)
    
    def __eq__(self, other):
        return self.__executor == other.__executor and self.__args == other.__args
        
    def tests(self):
        cur_dir = os.getcwd()
        
        executor = os.path.abspath(self.__executor)
        compiler.compile(executor)

        #TODO: fix this hack for java
        if lang_config.get_language(executor) != "java":
            exe_dir = tempfile.mkdtemp()
            os.chdir(exe_dir)
        else:
            exe_dir = cur_dir
        snapshot_before = Snapshot('.')
        invoker_result, retstdout, reterror = runner.run(executor, self.__args)
        if invoker_result.verdict != "OK":
            raise PleaseException(
                process_err_exit("Generator %s with args %s crashed with"
                    % (self.__executor, " ".join(self.__args)),
                    invoker_result.verdict, invoker_result.return_code,
                    retstdout, reterror))
        stdout = retstdout.decode()
        snapshot_after = Snapshot('.')
        os.chdir(cur_dir)
        
        diff = snapshot_before.get_changes(snapshot_after)
        
        mask = self.get_tags().get('mask')
        exclude = self.get_tags().get('exclude')
        tests, trash = self.diff_test_finder.tests(exe_dir, diff, stdout, self.__executor)
        tests.sort(key = test_file_sort.testfile_sorting_key)
        
        #remove trash
        for file in trash:
            os.remove(os.path.join(exe_dir, file))
        return tests
    
    def to_please_format(self):
        return ' '.join([self.get_prefix(), self.__executor, ' '.join(self.__args), self.get_suffix()]).strip()
