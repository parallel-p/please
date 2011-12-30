import unittest
from . import command_test_info
import os

class CommandTestInfoTest(unittest.TestCase):
    def test_simple_echo(self):
        a = command_test_info.CommandTestInfo(["echo"], ["1", "2", "3"])#["1", "2", "3"])#["1", "2", "3"], {"G" : "gurda"} )
        res = a.tests()
        
        self.assertEqual(open(res[0]).read(), "1 2 3")
        os.remove(res[0])
        
if __name__ == '__main__':
    unittest.main()