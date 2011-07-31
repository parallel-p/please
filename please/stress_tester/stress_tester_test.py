import unittest
import mox
import logging
import os.path
import io

import please.stress_tester.stress_tester
import please.test_config_parser.parser
import please.solution_runner.solution_runner
import please.checker_runner.checker_runner
import please.globalconfig as global_config
import please.solution_tester.package_config

class FakeInvokerReport():
    verdict = "OK"
    return_code = 0

class TestStressTester(unittest.TestCase):
    class FakeFile():
        def __init__(self):
            pass

        def __exit__(self, arg1, arg2, arg3):
            pass

        def __enter__(self):
            pass

        def read(self):
            return "ansdata"

        def write(self, data):
            pass

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.VerifyAll()

    def test_main_call_pass(self):
        self.mox.StubOutWithMock(logging, "getLogger")
        self.mox.StubOutWithMock(please.test_config_parser.parser.TestInfo, "__init__")
        self.mox.StubOutWithMock(please.tests_generator.tests_generator.TestsGenerator, "generate_all")
        self.mox.StubOutWithMock(please.solution_runner.solution_runner, "run_solution")
        self.mox.StubOutWithMock(os.path, "exists")
        self.mox.StubOutWithMock(io, "open")
        self.mox.StubOutWithMock(os, "remove")
        self.mox.StubOutWithMock(please.checker_runner.checker_runner, "run_checker")

        logger = self.mox.CreateMockAnything()
        logger.info("Test passed").AndRaise(please.stress_tester.stress_tester.StressCheckMatchException("test exception"))
        logger.error("Test failed")

        invoker = self.mox.CreateMockAnything()
        invoker.verdict.AndReturn('OK')

        please.test_config_parser.parser.TestInfo.__init__(1, mox.IgnoreArg()).AndReturn(None)
        please.tests_generator.tests_generator.TestsGenerator.generate_all().AndReturn(["test.path"])

        please.solution_runner.solution_runner.run_solution(mox.IgnoreArg()).MultipleTimes(2).AndReturn([FakeInvokerReport()])

        os.path.exists("test.path.out").MultipleTimes(2).AndReturn(True)
        os.path.exists(".please").AndReturn(True)

        f = self.FakeFile()
        io.open("test.path.out").MultipleTimes(2).AndReturn(f)

        io.open(os.path.join(".please", "correct.a"), "w").AndReturn(f)
        io.open(os.path.join(".please", "incorrect.a"), "w").AndReturn(f)

        os.remove("test.path.out").MultipleTimes(2)
        os.remove("test.path").MultipleTimes(2)

        please.checker_runner.checker_runner.run_checker(mox.IgnoreArg()).AndReturn([FakeInvokerReport()])

        logging.getLogger(mox.IgnoreArg()).AndReturn(logger)

        self.mox.ReplayAll()

        tester = please.stress_tester.stress_tester.StressTester({
            'checker' : 'check.cpp',
            'memory_limit' : '256',
            'time_limit' : '10'})

        tester(
            generator = "gen.cpp",
            solution = "sol.cpp",
            correct_solution = "sol_cor.cpp")

        self.assertRaises(please.stress_tester.stress_tester.StressCheckMatchException)

    def test_integration(self):
        current_dir = os.getcwd()
        try:
            os.chdir(os.path.join(global_config.root, "stress_tester", "test_problem"))
            tester = please.stress_tester.stress_tester.StressTester(please.solution_tester.package_config.PackageConfig.get_config('.', ignore_cache = True))
            tester(os.path.join('tests', 'generator.cpp'), os.path.join('solutions', 'solution_wrong.cpp'), os.path.join('solutions', 'solution.cpp'))
        finally:
            os.chdir(current_dir)
        self.assertRaises(please.stress_tester.stress_tester.StressCheckMatchException)

if __name__ == "__main__":
    unittest.main()
