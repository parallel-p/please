from ..solution_runner import solution_runner
from please.utils import cleanup
import os
import os.path
import random
from .. import globalconfig
from ..invoker.invoker import ExecutionLimits
from ..test_config_parser.parser import TestInfo
from ..tests_generator.tests_generator import TestsGenerator
from ..checker_runner import checker_runner
from ..executors.compiler import CompileError
import logging
import shutil
import io

class StressCheckException(Exception):
    pass

class StressCheckMatchException(Exception):
    pass

class StressCheckFail(Exception):
    pass

class StressRunException(Exception):
    pass

class StressTester():
    ''' This class created just to pass default.package config to __init__ (hack for matcher) '''

    __name__ = "StressTester"

    PLEASE_TEMP = ".please"
    CORRECT_OUT = "correct.a"
    INCORRECT_OUT = "incorrect.a"
    INPUT_TEST = "input.test"

    def __init__(self, config = None):
        ''' Config is .package object '''
        self.__config = config

    def __run_solution(self, solution, test_path):
        ''' Returns output [if invoker says OK] '''
        try:
            res = solution_runner.run_solution(solution_runner.SolutionInfo(
                source_path = solution,
                args = [],
                execution_limits = ExecutionLimits(float(self.__config["time_limit"]), float(self.__config["memory_limit"])),
                solution_config = self.__config,
                solution_input_file = test_path,
                solution_output_file = test_path + ".out"))

            if res[0].verdict != 'OK':
                self.logger.error("Run exception: %s is not OK, invoker returned %s, return code %s" % (solution, res[0].verdict, res[0].return_code))
                raise StressRunException()
        except CompileError:
            # TODO: add runerror
            self.logger.error("%s failed to compile" % solution)
            raise StressRunException()

        output_path = test_path + ".out"

        if os.path.exists(output_path):
            f = io.open(output_path)
            with f:
                out = f.read()
            os.remove(output_path)
            return out

        return ""


    def __generate_test(self, generator):
        ''' Creates random test '''
        newrand = random.randint(0, globalconfig.stress_up)
        test_info = TestInfo(1, "%s %s" % (generator, newrand))
        self.logger.warning("Random number for generator is: %s" % newrand)
        # generate ONE random test using given generator
        return TestsGenerator([test_info], "stress").generate(lambda x: True)[0]

    def __compare_outputs(self, input, correct_out, second_out, checker):
        ''' Compares two outputs with checker, returns True/False '''
        if not os.path.exists(".please"):
            os.mkdir(".please")
        correct_out_path = os.path.join(self.PLEASE_TEMP, self.CORRECT_OUT)
        f = io.open(correct_out_path, "w")
        with f:
            f.write(correct_out)

        second_out_path = os.path.join(self.PLEASE_TEMP, self.INCORRECT_OUT)
        f = io.open(second_out_path, "w")
        with f:
            f.write(second_out)

        res = checker_runner.run_checker(checker_runner.CheckerInfo(
            source_path = checker,
            input_file = input,
            correct_output = correct_out_path,
            program_output = second_out_path))

        # if checkfail, raise exception
        if not res[0].verdict in ['OK', 'RE']:
            self.logger.errror("Checkfail: Invoker returned %s, checker return code is %s, checker output %s" % (res[0].verdict, res[0].return_code, str(res[1])))
            raise StressCheckFail()

        # if return code == 0, solution accepted
        return res[0].return_code == 0

    def __check_solutions(self, solution, correct_solution, checker, test_path):
        ''' Runs our and correct solutions and checks output with checker '''
        try:
            output = self.__run_solution(solution, test_path)
        except StressRunException:
            self.logger.error("Solution %s failed to run" % solution)
            raise StressCheckException()

        try:
            correct = self.__run_solution(correct_solution, test_path)
        except StressRunException:
            self.logger.error("Correct solution %s failed to run" % correct_solution)
            raise StressCheckException()
        if not self.__compare_outputs(test_path, correct, output, checker):
            self.logger.error("Answers do not match, correct answer saved to %s, incorrect to %s, test saved to %s"
                %  (os.path.join(self.PLEASE_TEMP, self.CORRECT_OUT),
                    os.path.join(self.PLEASE_TEMP, self.INCORRECT_OUT),
                    os.path.join(self.PLEASE_TEMP, self.INPUT_TEST)))
            shutil.copy(test_path, os.path.join(self.PLEASE_TEMP, self.INPUT_TEST))
            raise StressCheckMatchException()

    def __call__(self, generator, solution, correct_solution = None):
        ''' Runs all process '''
        self.logger = logging.getLogger("please_logger.stress_tester.StressTester.test")

        if correct_solution is None:
            correct_solution = self.__config["main_solution"]
        try:
            while True:
                test_path = self.__generate_test(generator)
                try:
                    # solution is our [wrong] solution, correct_solution is 100% correct solution (it may be taken from config is not specified)
                    self.__check_solutions(solution, correct_solution, self.__config["checker"], test_path)
                    self.logger.info("Test passed")
                except (StressCheckMatchException, StressCheckException):
                    self.logger.error("Test failed")  
                    break
                except StressCheckFail:
                    self.logger.error("Check failed")
                    break
                finally:
                    if os.path.exists(test_path):
                        os.remove(test_path)
                    if os.path.exists(test_path+".out"):
                        os.remove(test_path+".out")
        except KeyboardInterrupt:
            self.logger.info("Interrupted")