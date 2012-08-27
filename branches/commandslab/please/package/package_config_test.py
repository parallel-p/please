import mox
import unittest
import os.path
import io

class PackageConfigTest(unittest.TestCase):
    
    def setUp(self):
        self.mox = mox.Mox()
        
    def tearDown(self):        
        self.mox.UnsetStubs()  
        self.mox.VerifyAll()  

    #TODO: fix this test
    #def test_package_config(self):        
    #    self.mox.StubOutWithMock(io, "open") 
    #    self.mox.StubOutWithMock(os.path, "exists")  
    #   
    #    m = io.open(mox.IgnoreArg(), encoding = mox.IgnoreArg()).AndReturn(self.mox.CreateMockAnything())
    #    m.read().AndReturn("please_version = 0.3")
    #    m.close().AndReturn(None)
    #    os.path.exists(mox.IgnoreArg()).AndReturn(True)
    #    os.path.exists(mox.IgnoreArg()).AndReturn(True)
    #   
    #   
    #    self.mox.ReplayAll()
    #   
    #    config = PackageConfig.get_config("myproblem")            
    #    self.assertEqual(config["please_version"], "0.1")
            
            
if __name__ == "__main__":
    unittest.main()
