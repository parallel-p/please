from please.test_config_parser.parser import TestInfo
from please.test_config_parser.parser import TestInfoType
import unittest
import mox
import os

class Test_TestInfo(unittest.TestCase):
    def setUp(self):
        self.mox=mox.Mox()
    
    def test_get_attributes(self):
        test_line = "[sample, scope=10, DP = 1] generator.cpp"
        self.mox.StubOutWithMock(os.path, "isfile")
        os.path.isfile("generator.cpp").AndReturn(True)
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists("generator.cpp").AndReturn(True)
        self.mox.ReplayAll()
        test_info_obj = TestInfo(0, test_line)
        test_attrib_dict = {"sample":None, "scope":"10", "DP":"1"}
        self.assertDictEqual(test_attrib_dict, test_info_obj.attributes)

    def tearDown(self):
#        self.mox.VerifyAll()
        self.mox.UnsetStubs()
        pass
        
    def test_type_getting(self):
        pass
        self.mox.StubOutWithMock(os.path, "isfile")
        os.path.isfile("generator.cpp").AndReturn(True)
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists("generator.cpp").AndReturn(True)
        self.mox.ReplayAll()
        test_line = "[sample, scope=10, DP = 1] generator.cpp"
        test_info_obj = TestInfo(0, test_line)
        self.assertEqual(test_info_obj.type, TestInfoType.GENERATOR)
"""        
        test_line = "[[sample, scope=10, DP = 1] WithoutExtension]"
        test_info_obj = TestInfo(0, test_line)
        self.assertEqual(test_info_obj.type, TestInfoType.FILE)
        
        test_line = "[[sample, scope=10, DP = 1] WithExtension.sample]"
        test_info_obj = TestInfo(0, test_line)
        self.assertEqual(test_info_obj.type, TestInfoType.FILE)
 
"""

if __name__ == '__main__':
    unittest.main()
