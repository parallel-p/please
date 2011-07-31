import unittest
import mox
from please.package.config import Config
import please.globalconfig as global_config
import os.path

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.maxDiff = None
    def test_getitem(self):
        conf = Config("""

        please_version = 0.1

        name = sloniki
        #dont know tags

        input =sloniki.in
        output = sloniki.out
        time_limit = 1 sec

        #randcomment
        memory_limit = 64 mb
        """)
        self.assertEqual("sloniki", conf["name"])
        self.assertEqual("0.1", conf["please_version"])
        self.assertEqual("64 mb", conf["memory_limit"])
        self.assertEqual("1 sec", conf["time_limit"])

    def test_contains(self):
        conf = Config("""

        please_version = 0.1

        name = sloniki
        #dont know tags

        input =sloniki.in
        output = sloniki.out
        time_limit = 1 sec

        #randcomment
        memory_limit = 64 mb
        """)

        self.assertTrue("output" in conf)

    def test_setitem(self):
        conf = Config("""

        please_version = 0.1

        name = sloniki
        #dont know tags

        input =sloniki.in
        output = sloniki.out
        time_limit = 1 sec

        #randcomment
        memory_limit = 64 mb
        """)
        
        conf["name"] = "slonik"
        conf["name"] = "slonik"
        self.assertEqual(conf["name"], "slonik")
        
    def test_isChanged(self):
        conf = Config("""
        
        please_version = 0.1

        name = sloniki
        #dont know tags

        input =sloniki.in
        output = sloniki.out
        time_limit = 1 sec

        #randcomment
        memory_limit = 64 mb
        """)
        
        conf["name"] = "slon"
        
        self.assertTrue(conf.isChanged)
        
    def test_delitem(self):
        conf = Config("""
        
        please_version = 0.1

        name = sloniki
        #dont know tags

        input =sloniki.in
        output = sloniki.out
        time_limit = 1 sec

        #randcomment
        memory_limit = 64 mb
        """)
        
        del conf["name"]
        self.assertFalse("name" in conf)
        
    def test_get_text(self):
        conf = Config(
"""please_version = 0.1

name = sloniki
#dont know tags

input = sloniki.in
output = sloniki.out
time_limit = 1 sec #
abacaba
abacaba1 #
abacaba2 #        23
 # 23
# 23
key = value # 23

#randcomment
memory_limit = 64 mb""")
        
        conf["name"] = "slonik"
        text = """please_version = 0.1

name = slonik
#dont know tags

input = sloniki.in
output = sloniki.out
time_limit = 1 sec #
abacaba
abacaba1 #
abacaba2 #        23
# 23
# 23
key = value # 23

#randcomment
memory_limit = 64 mb
"""
            
        self.assertEqual(conf.get_text(), text)
        conf["schoolboy"] = "stupid"
        conf["schoolboy"] = "extra stupid"
        
        text = """please_version = 0.1

name = slonik
#dont know tags

input = sloniki.in
output = sloniki.out
time_limit = 1 sec #
abacaba
abacaba1 #
abacaba2 #        23
# 23
# 23
key = value # 23

#randcomment
memory_limit = 64 mb
schoolboy = extra stupid
"""
        self.assertEqual(conf.get_text(), text)
        del conf["memory_limit"]

        text = """please_version = 0.1

name = slonik
#dont know tags

input = sloniki.in
output = sloniki.out
time_limit = 1 sec #
abacaba
abacaba1 #
abacaba2 #        23
# 23
# 23
key = value # 23

#randcomment
schoolboy = extra stupid
"""
        self.assertEqual(conf.get_text(), text)
        

        del conf["time_limit"]
        text = """please_version = 0.1

name = slonik
#dont know tags

input = sloniki.in
output = sloniki.out
#
abacaba
abacaba1 #
abacaba2 #        23
# 23
# 23
key = value # 23

#randcomment
schoolboy = extra stupid
"""
        self.assertEqual(conf.get_text(), text)
        
        conf["abacaba2"] = "z-function"
        text = """please_version = 0.1

name = slonik
#dont know tags

input = sloniki.in
output = sloniki.out
#
abacaba
abacaba1 #
abacaba2 = z-function #        23
# 23
# 23
key = value # 23

#randcomment
schoolboy = extra stupid
"""
        self.assertEqual(conf.get_text(), text)
        
        conf["wazzzuuup"] = None
        text = """please_version = 0.1

name = slonik
#dont know tags

input = sloniki.in
output = sloniki.out
#
abacaba
abacaba1 #
abacaba2 = z-function #        23
# 23
# 23
key = value # 23

#randcomment
schoolboy = extra stupid
wazzzuuup
"""
        self.assertEqual(conf.get_text(), text)

    def test_checker_global(self):
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists("test_checker.cpp").AndReturn(False)
        
        self.mox.ReplayAll()
        
        conf = Config("""
please_version = 0.1
checker = test_checker.cpp
""")
        self.assertEqual(conf["checker"], os.path.join(global_config.root, global_config.checkers_dir, "test_checker.cpp"))
        self.mox.UnsetStubs()
        
    def test_checker_local(self):
        self.mox.StubOutWithMock(os.path, "exists")
        os.path.exists("test_checker.cpp").AndReturn(True)
        
        self.mox.ReplayAll()
        
        conf = Config("""
please_version = 0.1
checker = test_checker.cpp
""")
        self.assertEqual(conf["checker"], "test_checker.cpp")
        self.mox.UnsetStubs()
        
    def test_simple_embedded_config(self):
        conf = Config("""
name = Pavel #some info
parameters = { #ololo
weight = 65 #normal
} #end
""")
        self.assertEqual(conf["parameters"]["weight"], "65")
        self.assertEqual(conf["name"], "Pavel")
        
    def test_difficult_embedded_config(self):
        conf = Config("""
company = LKSH
parallels = {
A = {
    sample_girl = Masha
    sample_boy = Ilya
    themes = {
        tree = AVL
        }
    }
P = {
   sample_boy = Pasha
   themes = {
       tests = mock
       }
    }
    conf = conf
}
""")
        self.assertEqual(conf["company"], "LKSH")
        self.assertEqual(conf["parallels"]["A"]["sample_girl"], "Masha")
        self.assertEqual(conf["parallels"]["A"]["sample_boy"], "Ilya")
        self.assertEqual(conf["parallels"]["P"]["sample_boy"], "Pasha")
        self.assertEqual(conf["parallels"]["A"]["themes"]["tree"], "AVL")
        self.assertEqual(conf["parallels"]["P"]["themes"]["tests"], "mock")
        self.assertEqual(conf["parallels"]["conf"], "conf")
        
    def test_keywords(self):
        conf = Config("""
config = {
    solution = {
    expected_verdicts = TL, OK
    }
    solution = {
    possible_verdicts = WA, ML
    }
}
""")
        self.assertEqual(conf["config"]["solution"][0]["expected_verdicts"], ["TL", "OK"])
        self.assertEqual(conf["config"]["solution"][1]["possible_verdicts"], ["WA", "ML"])
        
    def test_get_text_difficult(self):
        conf = Config("""
config = { # first comment
    hello # second
    #to be
    solution = { # i'm
        expected_verdicts = ML, TL #lovin'
        } # it
    solution = { # masha
    possible_verdicts = A, B, C, D #why?
    #to be
    } # pasha
    #or
    #not
} # korova
""")
        self.assertEqual(conf.get_text(), """
config = { # first comment
    hello # second
    #to be
    solution = { # i'm
        expected_verdicts = ML, TL #lovin'
        # it
    }
    solution = { # masha
        possible_verdicts = A, B, C, D #why?
        #to be
        # pasha
    }
    #or
    #not
    # korova
}
""")                
    def test_deleting(self):
        conf = Config("""el1 = a # hi
        el2 = b # hello
        el3 = v
        config = {
            #why
            
            solution = { #it's
                #so
                expected_verdicts = ML, TL #unexpected
                possible_verdicts = OK # cute
                el3 = WA # opa c
                
            }#bye
        }#bye""")
        del conf["el2"]
        del conf["el3"]
        del conf["config"]["solution"]
        self.assertEqual(conf.get_text(), """el1 = a # hi
# hello
config = {
    #why
    
    #bye
}
""")
    
    def test_set_sol(self):
        conf = Config("""please = 0.1
input = a.in
output = a.out
""")
        conf2 = Config("""expected_verdicts = ML, TL
possible_verdicts = OK""")
        conf["solution"] = [conf2,]
        self.assertEqual(conf.get_text(), """please = 0.1
input = a.in
output = a.out
solution = {
    expected_verdicts = ML, TL
    possible_verdicts = OK
}
""")
    def test_set(self):
        conf = Config("""
conf = {
solution = {
    expected_verdicts = ML, TL #cmo
    }
solution = {#abc
    possible_verdicts = OK
    }#avb
solution = {
    input = "peen"
    }
    
}""")
        conf["conf"].delete("solution", 1)
        conf2 = Config("")
        conf2["expected_verdicts"] = ["ML", "OK"]
        conf["conf"].set("solution", conf2, None, True)
        self.assertEqual(conf.get_text(), """
conf = {
    solution = {
        expected_verdicts = ML, TL #cmo
    }
    solution = {
        input = "peen"
    }
    
    solution = {
        expected_verdicts = ML, OK
    }
}
""")
    def test_set_solution(self):
        package_config = Config("""please_version = 0.1
my_sister = Liza""")
        for basename in range(5):
            config_file  = Config("")
            config_file ["source"] = "solutions." + str(basename)
            config_file ["expected_verdicts"] = ["OK"]  
            config_file ["possible_verdicts"] = ["ML"]
            package_config.set("solution", config_file, None, True)
        self.assertEqual(package_config.get_text(), """please_version = 0.1
my_sister = Liza
solution = {
    source = solutions.0
    expected_verdicts = OK
    possible_verdicts = ML
}
solution = {
    source = solutions.1
    expected_verdicts = OK
    possible_verdicts = ML
}
solution = {
    source = solutions.2
    expected_verdicts = OK
    possible_verdicts = ML
}
solution = {
    source = solutions.3
    expected_verdicts = OK
    possible_verdicts = ML
}
solution = {
    source = solutions.4
    expected_verdicts = OK
    possible_verdicts = ML
}
""")
        
if __name__ == "__main__":
    unittest.main()
