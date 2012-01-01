import unittest
import mox
from ..test_config_parser import parser
from ..test_info import file_test_info, cmd_gen_test_info
import os

class TestObjectFactoryTest(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
    def test_command(self):
        t = parser.TestObjectFactory(1, "echo 17 mama").create()
        self.assertIsInstance(t, cmd_gen_test_info.CmdOrGenTestInfo)
        q = t.tests()
        self.assertEqual( open(q[0]).read(), '17 mama\n')
        os.remove(q[0])
        
    def test_stdgen(self):
        self.assertIsInstance(
            parser.TestObjectFactory(1, "gen.cpp 17 42 100500").create(), cmd_gen_test_info.CmdOrGenTestInfo)
    def test_nonexist_file(self):
        with self.assertRaises(EnvironmentError):
            parser.TestObjectFactory(1, "iwasbreaking.awindow").create()
            
    def test_exist_file(self):
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists(os.path.join(".","test.txt")).AndReturn(True)
        self.mox.ReplayAll()
        
        a = parser.TestObjectFactory(1, "[a = 17, b = c] test.txt").create()
        self.assertIsInstance(a, file_test_info.FileTestInfo)
        self.assertDictEqual(a.get_tags(), {"a":"17", "b":"c"})
        
    def tearDown(self):
        self.mox.VerifyAll()
        self.mox.UnsetStubs()
        
if __name__ == '__main__':
    unittest.main()
