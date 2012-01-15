import unittest
from please.language_configurator.dpr import DprLinuxConfigurator
from please.language_configurator.dpr import DprWindowsConfigurator
from please.language_configurator.dpr import get_dpr_configurator
from please.language_configurator.dpr import is_compilation_garbage

class DprLinuxConfiguratorTest(unittest.TestCase):
    def test_is_garbage(self):
        extensions_list = [".BPG", ".BPL", ".CFG", ".DCP", ".DCU", ".DDP", ".DFM", ".~DF", ".DOF", ".DPK", ".~DP", ".DSK",
                           ".DSM", ".DCI", ".DRO", ".DMT", ".DCT", ".OBJ", ".~PA", ".RES", ".RC", ".TODO", ".BAK", ".bpg", ".bpl", 
                           ".cfg", ".dcp", ".dcu", ".ddp", ".dfm", ".~df", ".dof", ".dpk", ".~dp", ".dsk", ".dsm", ".dci", 
                           ".dro", ".dmt", ".dct", ".obj", ".~pa", ".res", ".rc", ".todo", ".bak"]
        
        dpr_linux_configurator = DprLinuxConfigurator()
        dpr_win_configurator = DprWindowsConfigurator()
        
        #simple extension test
        for extension in extensions_list :
            self.assertTrue(dpr_linux_configurator.is_compile_garbage("project" + extension))
        self.assertFalse(dpr_linux_configurator.is_compile_garbage("\windows\documents\sample_file "))
        self.assertFalse(dpr_linux_configurator.is_compile_garbage("\windows\documents\sample_file.dpr"))
        #case tests
        self.assertFalse(dpr_win_configurator.is_compile_garbage("\windows\documents\sample_file.Dpr"))
        self.assertFalse(dpr_win_configurator.is_compile_garbage("\windows\documents\sample_file.dPR"))
        self.assertFalse(dpr_win_configurator.is_compile_garbage("\windows\documents\sample_file.DPR"))              
                                     
    def test_get_compile_command(self) :
        #linux command test
        dpr_linux_configurator = DprLinuxConfigurator()
        self.assertEqual(["fpc",  "project.dpr"], dpr_linux_configurator.get_compile_command("project.dpr"))
        self.assertEqual(["./project"], dpr_linux_configurator.get_run_command("project.dpr"))
        #windows command test
        dpr_win_configurator = DprWindowsConfigurator()
        self.assertEqual(["dcc32.exe", "-cc", "project.dpr"], dpr_win_configurator.get_compile_command("project.dpr"))
        self.assertEqual(["project.exe"], dpr_win_configurator.get_run_command("project.dpr"))
                
if __name__ == '__main__':
    unittest.main()

