import os
import re
from ..test_info.test_file import FileTestFile, StrTestFile

class DiffTestFinder:
    """
    Takes diff of problem's directory before and after generator executing,
    may take mask of tests and may take mask of files, that exactly are not tests
    Requires path to directory in which generator executed.
    May take a name of file of redirected stdout of generator, if there is no test
    generated in filesystem.
    Masks are in python.re syntax.
    Returns list of test relative paths from execute_dir.
    
    Example:
    test_finder = DiffTestFinder('directory_where_generator_executed', '.*\\.in$', '\\.\\./trash.*\\.in$')
    (mask in cmd or bash corresponds with *.in, exclude corresponds with ../trash*.in)
    tests = test_finder.tests(diff, 'generator_stdout.out')
    tests == ['../01.in', '../02.in', '03.in', 'tests/100500.in']
    
    Warning: read python re syntax carefully before use!
    """
    # TODO: probably it's better to use fnmatch?
    def __init__(self, mask=None, exclude=None):
        #mask and exclude is a string
        self.mask = re.compile(mask or '')
        self.exclude = re.compile(exclude or '$^')
        
    def tests(self, exe_dir, diff, stdout=None, generator=None):
        """
        diff is a list of files, stdout - redirected stdout of generator,
        returns names of test files, if stdout == None and no files found returns []
        """
        cur_diff=diff[1][:] # diff[0] is new dirs, diff[1] is new files
        new_diff = []
        trash = []
        
        for file in cur_diff: # make paths relative from execute_dir
            relpath = os.path.relpath(file, exe_dir)
            if self.mask.match(relpath) and not self.exclude.match(relpath):
                new_diff.append(FileTestFile(file, relpath))
            else:
                trash.append(file)
        
        if not new_diff and stdout is not None:
            return [StrTestFile(stdout, 'stdout of {0}'.format(generator or 'generator'))], trash
        else:
            return new_diff, trash
