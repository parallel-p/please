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
    
    Example:
    test_finder = DiffTestFinder('directory_where_generator_executed', '.*\\.in$', '\\.\\./trash.*\\.in$')
    (mask in cmd or bash corresponds with *.in, exclude corresponds with ../trash*.in)
    tests = test_finder.tests(diff, 'generator_stdout.out')
    tests == ['../01.in', '../02.in', '03.in', 'tests/100500.in']
    
    Warning: read python re syntax carefully before use!
    """
    def __init__(self, execute_dir, mask=None, exclude=None):
        #mask and exclude is a string, execute_dir - string, directory, in which generator worked
        self.execute_dir = execute_dir
        self.mask = mask
        self.exclude = exclude
        
    def match(self, file, mask):
        return re.match(mask, file) is not None
    
    def get_desc(self):
        return self.__desc
    
    def tests(self, diff, stdout=None):
        """
        diff is a list of files, stdout - file of redirected stdout of generator,
        returns names of test files, if stdout == None and no files found returns []
        """
        cur_diff=diff[1][:] #diff[0] is new dirs, diff[1] is new files
        new_diff = []
        
        for file in cur_diff: #make paths relative from execute_dir
            new_diff.append(os.path.relpath(file, self.execute_dir))
        cur_diff = new_diff[:]
        new_diff = []
        
        if self.exclude is not None:
            for file in cur_diff:
                if not self.match(file, self.exclude):
                    new_diff.append(file)
            cur_diff = new_diff[:]
            new_diff = []

        if self.mask is not None:
            for file in cur_diff:
                if self.match(file, self.mask):
                    new_diff.append(file)
            cur_diff = new_diff[:]
            new_diff = []
            
        if not cur_diff and stdout is not None:
            self.__desc = ['standard generator output']
            return [stdout]
        else:
            self.__desc = cur_diff
            return cur_diff
        