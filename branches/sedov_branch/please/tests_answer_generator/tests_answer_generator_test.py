from ..answers_generator import answers_generator
import io
from ..tests_answer_generator import tests_answer_generator
from ..validator_runner import validator_runner
from ..solution_runner import solution_runner
from ..invoker.invoker import ExecutionLimits
from ..tests_generator import tests_generator
from ..test_config_parser import parser
from ..well_done import well_done
from ..package import package_config
import unittest
import os
import mox
        
class Tester (unittest.TestCase):
    def setUp (self):
        self.mox = mox.Mox()
        
    def tearDown(self):
        self.mox.UnsetStubs()

    class WellDoneMock():
        def __init__(self, key):
            self.__key = key
        def check(self, file, fix_inplace):
            return (well_done.OK, [])
    
    def test_generate (self):
        generator = tests_answer_generator.TestsAndAnswersGenerator()
        
        test_info = self.mox.CreateMockAnything()
        test_info.command = ("file",[])
        test_list = [test_info]
        
        val_res = self.mox.CreateMockAnything()
        val_res.return_code = 0
        val_res.verdict = "OK"
        
        well_done = self.WellDoneMock("key")
        f = self.mox.CreateMockAnything()
        generator._TestsAndAnswersGenerator__create_well_done = f
        f(generator, "well_done_test").AndReturn(well_done)              
        f(generator, "well_done_test").AndReturn(well_done)              
        
        ftcp = self.mox.CreateMock(parser.FileTestConfigParser)
        ftcp.get_test_info_objects().AndReturn(test_list)
        self.mox.StubOutWithMock(parser, "FileTestConfigParser")
        parser.FileTestConfigParser(well_done).AndReturn(ftcp)
        
        tests_gen = self.mox.CreateMock(tests_generator.TestsGenerator)
        tests_gen.generate_all().AndReturn([".tests/1"])
        self.mox.StubOutWithMock(tests_generator, "TestsGenerator")
        tests_generator.TestsGenerator(test_list).AndReturn(tests_gen)
        
        dic = {"input":"stdin", "output":"stdout", "validator" : "val", "solution" : "sol", "main_solution" : "ms", "memory_limit" : "32", 'solution' : [ {'source' : 'mc'} ], 'checker' : 'check.cpp', 'time_limit': 2, 'memory_limit': 64}
        
        self.mox.StubOutWithMock(package_config.PackageConfig, "get_config")
        package_config.PackageConfig.get_config().MultipleTimes().AndReturn(dic)
        
        self.mox.StubOutWithMock(validator_runner, "validate")
        validator_runner.validate(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(
                (val_res, 'stdout', 'stderr'))
        
        answers_gen = self.mox.CreateMock(answers_generator.AnswersGenerator)
        answers_gen.generate(['.tests/1'], 'ms', [], 
                             {'memory_limit': 64, 'main_solution': 'ms', 
                              'validator': 'val', 'output': 'stdout', 
                              'time_limit': 2, 'input': 'stdin', 
                              'checker': 'check.cpp', 'solution': [{'source': 'mc'}]}).AndReturn([".tests/1.a"])
        
        self.mox.StubOutWithMock(answers_generator, "AnswersGenerator")
        answers_generator.AnswersGenerator().AndReturn(answers_gen)
                
        self.mox.ReplayAll()
        
        for t, p in generator.generate_all():
            self.assertEqual((t, p), (".tests/1", ".tests/1.a"))
        
        self.mox.VerifyAll()
        
if __name__ == '__main__':
    unittest.main()

        
        
