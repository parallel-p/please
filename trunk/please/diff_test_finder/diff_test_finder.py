import os
import re

class DiffTestFinder:
    """
    Takes diff of problem's directory before and after generator executing,
    may take mask of tests and may take mask of files, that exactly are not tests
    Requires path to directory in which generator executed.
    May take a name of file of redirected stdout of generator, if there is no test
    generated in filesystem.
    Masks are in python.re syntax.
    Returns list of test relative paths from execute_dir.
    
    Warning: if ways from diff are relative (now it means if diff was taked from directory
    with relative path) it would be better not change directory before using this class,
    in other way os.path.relpaths(<filename from not current directory>, <execute_dir>) must
    work incorrectly.
    
    Example:
    test_finder = DiffTestFinder('directory_where_generator_executed', '.*/.*\\.in', '\\.\\./trash.*\\.in')
    (mask in cmd or bash corresponds with */*.in, exclude corresponds with ../trash*.in)
    tests = test_finder.tests(diff, 'generator_stdout.out')
    tests == ['../01.in', '../02.in', '03.in', 'tests/100500.in']
    """
    def __init__(self, execute_dir, mask=None, exclude=None):
        #mask and exclude is a string, execute_dir - string, directory, in which generator worked
        self.execute_dir = execute_dir
        self.mask = mask
        self.exclude = exclude
        
    def match(self, filename, mask):
        return re.match(mask, file) is not None
    
    def tests(self, diff, stdout=None):
        #diff is a list of files, stdout - file of redirected stdout of generator, returns names of test files
        cur_diff=diff[1][:] #diff[0] is new dirs, diff[1] is new files
        new_diff = []
        
        for file in cur_diff: #make paths relative from execute_dir
            new_diff.append(os.path.relpath(file, self.execute_dir))
        cur_diff = new_diff[:]
        
        if exclude is not None:
            for file in cur_diff:
                if not self.match(file, exclude):
                    new_diff.append(i)
            cur_diff=new_diff[:]

        if mask is not None:
            for file in cur_diff:
                if self.match(file, mask):
                    new_diff.append(i)
            cur_diff=new_diff[:]

        if not cur_diff and stdout is not None:
            return [stdout]
        else:
            return cur_diff