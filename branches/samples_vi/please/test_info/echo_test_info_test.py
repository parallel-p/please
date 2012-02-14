import unittest
from . import echo_test_info
import os
import shutil

class CmdOrGenTestInfo(unittest.TestCase):
    
    def test_generator(self):
        stdir = os.getcwd()
        a = echo_test_info.EchoTestInfo("blue dog")
        res = a.tests()
        
        #TODO:what is res[0]?
        with open(res[0]) as res_file:
            self.assertEqual(res_file.read(), "blue dog\n")
        os.remove(res[0])
        
if __name__ == '__main__':
    unittest.main()
