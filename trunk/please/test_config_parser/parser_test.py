import unittest
import mox
from ..test_config_parser import parser
from ..test_info import file_test_info, cmd_gen_test_info
import os

class TestObjectFactoryTest(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
    def test_command(self):
        t = parser.TestObjectFactory.create(1, "echo",  ["17",  "mama"])
        self.assertIsInstance(t, cmd_gen_test_info.CmdOrGenTestInfo)
        q = t.tests()
        self.assertEqual( open(q[0]).read(), '17 mama\n')
        os.remove(q[0])
        
    def test_stdgen(self):
        self.assertIsInstance(
            parser.TestObjectFactory.create(1, "gen.cpp", ["17", "42", "100500"]), cmd_gen_test_info.CmdOrGenTestInfo)
    def test_nonexist_file(self):
        with self.assertRaises(EnvironmentError):
            parser.TestObjectFactory.create(1, "iwasbreaking.awindow", [])
            
    def test_exist_file(self):
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists(os.path.join(".","test.txt")).AndReturn(True)
        self.mox.ReplayAll()
        
        a = parser.TestObjectFactory.create(1, "test.txt", [], {"a":"17", "b":"c"})
        self.assertIsInstance(a, file_test_info.FileTestInfo)
        self.assertDictEqual(a.get_tags(), {"a":"17", "b":"c"})
        
    def test_parse(self):
        a = parser.TestConfigParser("test_problems/generator/main.cpp 1 2 3\n[sample]test_problems/generator/main.cpp happy new year")
        self.assertEqual(a.get_binaries(), ["test_problems/generator/main.cpp"])
        b = a.get_test_info_objects()
        
        t = b[0].tests()
        with open(t[0]) as f:
            self.assertEqual(f.read(), "1 2 3 ")
        
        t = b[1].tests()
        with open(t[0]) as f:
            self.assertEqual(f.read(), "happy new year ")
                
        
    def tearDown(self):
        self.mox.VerifyAll()
        self.mox.UnsetStubs()
        
if __name__ == '__main__':
    unittest.main()
