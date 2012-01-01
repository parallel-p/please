import unittest
from . import cmd_gen_test_info
import os
import shutil

class CmdOrGenTestInfo(unittest.TestCase):
    
    def test_simple_echo(self):
        a = cmd_gen_test_info.CmdOrGenTestInfo("echo", ["1", "2", "3"], {"G" : "gurda"} )
        res = a.tests()
        
        self.assertEqual(open(res[0]).read(), "1 2 3\n")
        os.remove(res[0])
        
        self.assertEqual(a.to_please_format(), "[G = gurda] echo 1 2 3")
        
    def test_generator(self):
        stdir = os.getcwd()
        a = cmd_gen_test_info.CmdOrGenTestInfo("test_problems/generator/main.cpp", ["blue", "dog"])
        res = a.tests()
        
        self.assertEqual(open(res[0]).read(), "blue dog ")
        os.remove(res[0])
        
if __name__ == '__main__':
    unittest.main()