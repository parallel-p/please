import unittest
from please.lang_config.dpr import DprFreePascalConfig, DprDelphiConfig
from please.lang_config import utils

class DprLinuxConfiguratorTest(unittest.TestCase):
    def test_is_garbage(self):
        extensions_list = [".BPG", ".BPL", ".CFG", ".DCP", ".DCU", ".DDP", ".DFM", ".~DF", ".DOF", ".DPK", ".~DP", ".DSK",
                           ".DSM", ".DCI", ".DRO", ".DMT", ".DCT", ".OBJ", ".~PA", ".RES", ".RC", ".TODO", ".BAK", ".bpg", ".bpl", 
                           ".cfg", ".dcp", ".dcu", ".ddp", ".dfm", ".~df", ".dof", ".dpk", ".~dp", ".dsk", ".dsm", ".dci", 
                           ".dro", ".dmt", ".dct", ".obj", ".~pa", ".res", ".rc", ".todo", ".bak"]
        
        linux = DprFreePascalConfig('sample_file.dpr')
        win = DprDelphiConfig('sample_file.dpr')
        
        #simple extension test
        for extension in extensions_list :
            self.assertTrue(linux.is_compile_garbage("project" + extension))
        self.assertFalse(linux.is_compile_garbage("\windows\documents\sample_file"))
        self.assertFalse(linux.is_compile_garbage("\windows\documents\sample_file.dpr"))
        #case tests
        self.assertFalse(win.is_compile_garbage("\windows\documents\sample_file.Dpr"))
        self.assertFalse(win.is_compile_garbage("\windows\documents\sample_file.dPR"))
        self.assertFalse(win.is_compile_garbage("\windows\documents\sample_file.DPR"))              
                                     
    def test_get_compile_command(self) :
        #linux command test
        linux = DprFreePascalConfig('project.dpr')
        self.assertEqual((["fpc",  "-Mdelphi", "project.dpr"],), linux.compile_commands)
        self.assertEqual(["./project"], linux.run_command)
        #windows command test
        win = DprDelphiConfig('project.dpr')
        self.assertEqual((["dcc32.exe", "-cc", "project.dpr"],), win.compile_commands)
        #self.assertEqual(["project.exe"], win.run_command) # hard decisions in utils
                
if __name__ == '__main__':
    unittest.main()

