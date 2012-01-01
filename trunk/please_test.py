import os
import sys
import shutil
import unittest
import filecmp
from please.command_line.template import Template
from please.command_line.matcher import Matcher
from please.command_line import generate_tests
from please.command_line.commands import print_help
from please.command_line.generate_tests import generate_tests, generate_tests_with_tags
from please.checkers.standard_checkers_utils import add_standard_checker_to_solution
from please.template import problem_template_generator as problem_gen
from please.solution_tester import package_config
from please.tags import add_tags, show_tags, clear_tags
from please.latex import latex_tools
from please.svn import delete_problem
import please.globalconfig as globalconfig

class PleaseTest(unittest.TestCase):
    def ifed(self):
        if os.path.exists("problem_test"):
            delete_problem("problem_test")
    def setUp(self):
        self.ifed()
        self.__matcher = Matcher()
        self.__matcher.add_handler(Template(["create", "problem", "#shortname"]), problem_gen.generate_problem, True)
        self.__matcher.matches("create problem problem_test".split())
        
    def tearDown(self):
        self.ifed()
        if os.path.exists("problem_test"):
            delete_problem("problem_test")
    
    def test_problem_creation(self):
        """ Checks command 'create problem problem_name' """
        self.assertTrue(os.path.exists("problem_test"))
        self.assertTrue(os.path.exists(os.path.join("problem_test", "solutions")))
        self.assertTrue(os.path.exists(os.path.join("problem_test", "statements")))
        self.assertTrue(os.path.exists(os.path.join("problem_test", "default.package")))
        self.assertTrue(os.path.exists(os.path.join("problem_test", "tests.please")))
            
    def test_add_tags(self):
        """ Checks command 'add tags tag1 tag2 ... tagN' """
        
        start_dir = os.getcwd()
        os.chdir("problem_test")
        #package_config.PackageConfig.configs_dict = {}
        self.__matcher.add_handler(Template(["add", "tag|tags", "@tags"]), add_tags, True)
        self.__matcher.matches("add tags tag1 tag2 tag3 tag4".split())
              
        open_config = package_config.PackageConfig.get_config(ignore_cache = True)
        
        
        os.chdir(start_dir)
        
        self.assertEqual(open_config["tags"], "tag1; tag2; tag3; tag4")
        
        
    def test_show_tags(self):
        """ Checks command 'show tags' """
        
        start_dir = os.getcwd()
        os.chdir("problem_test")
        
        self.__matcher.add_handler(Template(["add", "tag|tags", "@tags"]), add_tags, True)
        self.__matcher.matches("add tags tag1 tag2 tag3 tag4".split())
        
        with open("temp.txt", "a+") as std_to_file:
            saveout = sys.stdout
            sys.stdout = std_to_file
            
            self.__matcher.add_handler(Template(["show", "tags"]), show_tags, True)
            self.__matcher.matches("show tags".split())
            
            tags_from_std = std_to_file.read().split("\n")[0]
        sys.stdout = saveout
        
        open_config = package_config.PackageConfig.get_config(ignore_cache = True) 
        os.chdir(start_dir)
        self.assertEqual(open_config["tags"], tags_from_std)
    
    def test_clear_tags(self):
        """ Checks command 'clear tags' """

        start_dir = os.getcwd()
        os.chdir("problem_test")
        
        self.__matcher.add_handler(Template(["add", "tag|tags", "@tags"]), add_tags, True)
        self.__matcher.matches("add tags tag1 tag2 tag3 tag4".split())
        
        self.__matcher.add_handler(Template(["clear", "tags"]), clear_tags, True)
        self.__matcher.matches("clear tags".split())
        
        with open("temp.txt", "a+") as std_to_file:
            saveout = sys.stdout
            sys.stdout = std_to_file
            
            self.__matcher.add_handler(Template(["show", "tags"]), show_tags, True)
            self.__matcher.matches("show tags".split())
            
            ttt = std_to_file.read()
            tags_from_std = ttt.split("\n")[0]
        sys.stdout = saveout

        open_config = package_config.PackageConfig.get_config(ignore_cache = True)
        os.chdir(start_dir)
        self.assertEqual(tags_from_std, "")
        
        
        
    def test_add_standard_checker(self):
        """ Checks command 'add standard checker checker_name' """
        start_dir = os.getcwd()
        os.chdir("problem_test")
        
        open_config = package_config.PackageConfig.get_config()
        self.__matcher.add_handler(Template(["add", "standard", "checker", "#checker"]), add_standard_checker_to_solution, True)
        self.__matcher.matches("add standard checker test_checker".split())
        

        os.chdir(start_dir)
        self.assertEqual(os.path.join(start_dir, "please", "checkers", "test_checker.cpp"), open_config["checker"])
        
        
    def test_generate_statement(self):
        """ Checks command 'generate statement' """
        
        start_dir = os.getcwd()
        #shutil.copy(os.path.join("island", "statements", "default.ru.pdf"), ".")
        test_problem_dir = os.path.join("test_problems", "island")
        os.chdir(test_problem_dir)
        if os.path.exists(os.path.join("statements", "default.ru.pdf")):
            os.remove(os.path.join("statements", "default.ru.pdf"))
        
        self.__matcher.add_handler(Template(["generate", "statement"]), latex_tools.generate_contest, True)
        self.__matcher.matches("generate statement".split())
        
        os.chdir(start_dir)
        self.assertTrue(os.path.exists(os.path.join(test_problem_dir, "statements", "default.ru.pdf")))
        
    def test_help(self):
        """ Checks command 'help' """

        open_config = package_config.PackageConfig.get_config('.')
        in_problem_folder = (package_config != False)
        globalconfig.in_problem_folder = in_problem_folder

        self.__matcher.add_handler(Template(["help"]), print_help, True)
        self.__matcher.matches("help".split())
        
        
if __name__ == "__main__":
    unittest.main()
