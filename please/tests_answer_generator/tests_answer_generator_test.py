from please.answers_generator import answers_generator
import io
from please.tests_answer_generator import tests_answer_generator
from please.validator_runner import validator_runner
from please.solution_runner import solution_runner
from please.invoker.invoker import ExecutionLimits
from please.tests_generator import tests_generator
from please.test_config_parser import parser
from please.solution_tester import package_config
import unittest
import mox
        
class Tester (unittest.TestCase):
    def setUp (self):
        self.mox = mox.Mox()
        
    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.VerifyAll()
    
    def test_generate (self):
        test_info = self.mox.CreateMockAnything()
        test_info.command = ("file",[])
        test_list = [test_info]
        
        val_res = self.mox.CreateMockAnything()
        val_res.return_code = 0
        val_res.verdict = "OK"
        
        self.mox.StubOutWithMock(parser, "parse_test_config")
        parser.parse_test_config().AndReturn(test_list)
        
        tests_gen = self.mox.CreateMock(tests_generator.TestsGenerator)
        tests_gen.generate_all().AndReturn(["file"])
        
        self.mox.StubOutWithMock(tests_generator, "TestsGenerator")
        tests_generator.TestsGenerator(test_list).AndReturn(tests_gen)
        
        dic = {"input":"stdin", "output":"stdout", "validator" : "val", "solution" : "sol", "main_solution" : "ms", "memory_limit" : "32"}
        
        self.mox.StubOutWithMock(package_config.PackageConfig, "get_config")
        package_config.PackageConfig.get_config().AndReturn(dic)
        
        self.mox.StubOutWithMock(validator_runner, "validate")
        validator_runner.validate(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn((val_res, []))
        
        answers_gen = self.mox.CreateMock(answers_generator.AnswersGenerator)
        answers_gen.generate(["file"], "ms", [], dic)
        
        self.mox.StubOutWithMock(answers_generator, "AnswersGenerator")
        answers_generator.AnswersGenerator().AndReturn(answers_gen)
                
        self.mox.ReplayAll()
        
        generator = tests_answer_generator.TestsAndAnswersGenerator()
        self.assertEqual(generator.generate_all(), (0,[("file","OK")]))
        
if __name__ == '__main__':
    unittest.main()

        
        
