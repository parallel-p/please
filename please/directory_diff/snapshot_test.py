import unittest
from .snapshot import Snapshot
from .snapshot import get_changes
import os
import shutil

class TestSnapshot(unittest.TestCase):
    
    def setUp(self):
        if not os.path.exists("temp_files"):
            os.mkdir("temp_files")
        if not os.path.exists(os.path.join("temp_files", "to_ignore")):
            os.mkdir(os.path.join("temp_files", "to_ignore"))
            
    def tearDown(self):
        shutil.rmtree("temp_files")
        if os.path.exists(os.path.join("temp_files", "to_ignore")):
            shutil.rmtree(os.path.join("temp_files", "to_ignore"))
        
    def test_get_changes(self):
        # Make a snapshot of directory before creating a new file        
        snap1 = Snapshot("temp_files", [], False) 
        
        # Create a new file
        open("temp_files/temp.py", "w").close()
        
        # Make a snapshot of directory after creating a new file
        snap2 = Snapshot("temp_files", [], False)
        
        self.assertEqual(get_changes(snap1, snap2), [ [], [os.path.join(os.getcwd(), os.path.join("temp_files", "temp.py")) ] ])
        
        # Clean up
        os.remove("temp_files/temp.py")        
      
    def test_ignore_dir(self):
        # Make a snapshot of directory with a folder inside to ignore 
        snap1 = Snapshot("temp_files", ["to_ignore"], False) 
        
        # Make a snapshot of directory without a folder inside to ignore 
        snap2 = Snapshot("temp_files", [], False)
        
        self.assertEqual(get_changes(snap1, snap2), [[ os.path.join(os.getcwd(), os.path.join("temp_files", "to_ignore")) ],[]])
    
if __name__ == '__main__':
    unittest.main()
