import mox
from please.executors.trash_remover import remove_trash
import unittest
import os

class RemoveTrashTest(unittest.TestCase):
    def is_trash(filename):
        return filename.endswith(".trash")
    
    def setUp(self):
        self.mox = mox.Mox()
    
    def tearDown(self):
        self.mox.VerifyAll()
        self.mox.UnsetStubs()

        
    def test_remover(self):
        
        self.mox.StubOutWithMock(os,"remove")
        diff = ["C:\wsvn\work\ololo.exe", "C:\wsvn\work\ololo.trash", 
                "C:\wsvn\work\ololo.pdb.trash", "C:\wsvn\work\ololo",
                "C:\wsvn\work\log.ini.trash"]
        os.remove(diff[1])
        os.remove(diff[2])
        os.remove(diff[4])
        
        self.mox.ReplayAll()
        remove_trash (diff,RemoveTrashTest.is_trash)
        
if __name__ == '__main__':
     unittest.main()       