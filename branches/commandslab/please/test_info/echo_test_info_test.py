import unittest
from . import echo_test_info
import os
import shutil

class CmdOrGenTestInfo(unittest.TestCase):
    
    def test_generator(self):
        stdir = os.getcwd()
        a = echo_test_info.EchoTestInfo("blue dog")
        res = a.tests()
        
        self.assertEqual(res[0].contents(), "blue dog\n")
        
if __name__ == '__main__':
    unittest.main()
