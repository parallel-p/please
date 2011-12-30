import unittest
import mox
from . import parser2
from ..test_info import file_test_info, filegen_test_info, stdgen_test_info, command_test_info
import os

class TestObjectFactoryTest(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
    def test_command(self):
        self.assertIsInstance(
            parser2.TestObjectFactory(1, "echo 1 2 3").create(), command_test_info.CommandTestInfo)
    def test_stdgen(self):
        self.assertIsInstance(
            parser2.TestObjectFactory(1, "gen.cpp 17 42 100500").create(), stdgen_test_info.StdGenTestInfo)
    def test_nonexist_file(self):
        with self.assertRaises(EnvironmentError):
            parser2.TestObjectFactory(1, "iwasbreaking.awindow").create()
            
    def test_exist_file(self):
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists(os.path.join(".","test.txt")).AndReturn(True)
        self.mox.ReplayAll()
        
        a = parser2.TestObjectFactory(1, "[a = 17, b = c] test.txt").create()
        self.assertIsInstance(a, file_test_info.FileTestInfo)
        self.assertDictEqual(a.get_tags(), {"a":"17", "b":"c"})
        
    def tearDown(self):
        self.mox.VerifyAll()
        self.mox.UnsetStubs()
        
if __name__ == '__main__':
    unittest.main()
