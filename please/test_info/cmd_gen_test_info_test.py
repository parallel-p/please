import unittest
from please.test_info import cmd_gen_test_info
import os
import shutil

class CmdOrGenTestInfo(unittest.TestCase):
    
    def test_simple_echo(self):
        a = cmd_gen_test_info.CmdOrGenTestInfo("echo", ["1", "2", "3"], {"G" : "gurda"} )
        res = a.tests()
        
        self.assertEqual(open(res[0]).read(), "1 2 3\n")
        os.remove(res[0])
        
        self.assertEqual(a.to_please_format(), "[G = gurda] echo 1 2 3")
        
    def test_generator(self):
        stdir = os.getcwd()
        os.makedirs('test_problems/generator/')
        f=open('test_problems/generator/main.cpp', 'w')
        f.write('#include <iostream>\n \
        #include <cstdio>\n \
        using namespace std;\n \
        int main(int argc, char *argv[]){\n \
        for (int i=1; i<argc; ++i) cout<<argv[i]<<\' \';\n \
        }')
        f.close()
        a = cmd_gen_test_info.CmdOrGenTestInfo("test_problems/generator/main.cpp", ["blue", "dog"])
        res = a.tests()
        
        self.assertEqual(open(res[0]).read(), "blue dog ")
        os.remove(res[0])
        shutil.rmtree('test_problems')
        
if __name__ == '__main__':
    unittest.main()