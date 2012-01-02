import unittest
import mox
from ..test_config_parser import parser
from ..test_info import file_test_info, cmd_gen_test_info, echo_test_info, python_test_info
import os

class TestObjectFactoryTest(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
    
    class WellDoneMock():
        def __init__(self, key):
            self.__key = key
        def check(self, file):
            return 0  
			        
    def test_command(self):
        well_done = self.WellDoneMock("key")
        t = parser.TestObjectFactory.create(well_done, 1, "echo",  ["17",  "mama"])
        self.assertIsInstance(t, echo_test_info.EchoTestInfo)
        q = t.tests()
        with open(q[0]) as test_file:
            self.assertEqual(test_file.read(), '17 mama\n')
        os.remove(q[0])
        
    def test_stdgen(self):
        well_done = self.WellDoneMock("key")
        self.assertIsInstance(
            parser.TestObjectFactory.create(well_done, 1, "gen.cpp", ["17", "42", "100500"]), cmd_gen_test_info.CmdOrGenTestInfo)
    def test_nonexist_file(self):
        well_done = self.WellDoneMock("key")
        with self.assertRaises(EnvironmentError):
            parser.TestObjectFactory.create(well_done, 1, "iwasbreaking.awindow", [])
            
    def test_exist_file(self):
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists(os.path.join(".","test.txt")).AndReturn(True)
        self.mox.ReplayAll()

        well_done = self.WellDoneMock("key")        
        a = parser.TestObjectFactory.create(well_done, 1, "test.txt", [], {"a":"17", "b":"c"})
        self.assertIsInstance(a, file_test_info.FileTestInfo)
        self.assertDictEqual(a.get_tags(), {"a":"17", "b":"c"})
        
    def test_parse(self):
        well_done = self.WellDoneMock("key")
        a = parser.TestConfigParser("test_problems/generator/main.cpp 1 2 3\n[sample]test_problems/generator/main.cpp happy new year", well_done)
        self.assertEqual(a.get_binaries(), [os.path.join("test_problems", "generator", "main.cpp")])
        b = a.get_test_info_objects()
        
        t = b[0].tests()
        with open(t[0]) as f:
            self.assertEqual(f.read(), "1 2 3 ")
        
        t = b[1].tests()
        with open(t[0]) as f:
            self.assertEqual(f.read(), "happy new year ")
    def test_python(self):
        a = parser.TestConfigParser("python 'ab'*  5")
        b = a.get_test_info_objects()
        t = b[0].tests()
        with open(t[0]) as f:
            self.assertEqual(f.read(), "ababababab")
    def test_python(self):
        a = parser.TestConfigParser("python hi")
        b = a.get_test_info_objects()
        with self.assertRaises(EnvironmentError) as ex:  
            t = b[0].tests()
    def tearDown(self):
        self.mox.VerifyAll()
        self.mox.UnsetStubs()
        
if __name__ == '__main__':
    unittest.main()
