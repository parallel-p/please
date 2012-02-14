from ..solution_runner import solution_runner
import os
import os.path
import random
from .. import globalconfig
from ..invoker.invoker import ExecutionLimits
from ..test_info import cmd_gen_test_info
from ..tests_generator.tests_generator import TestsGenerator
from ..checker_runner import checker_runner
from ..utils.exceptions import PleaseException
import logging
import shutil

class StressCheckException(PleaseException):
    pass

class StressCheckMatchException(PleaseException):
    pass

class StressCheckFail(PleaseException):
    pass

class StressRunException(PleaseException):
    pass

class StressTester():

    __name__ = "StressTester"

    PLEASE_TEMP = ".please"
    CORRECT_OUT = "correct.a"
    INCORRECT_OUT = "incorrect.a"
    INPUT_TEST = "input.test"
    #TODO: sometimes some garbage lefts (correct.a, incorrect.a when we have RunExc)
    def __init__(self, config = None):
        ''' Config is .package object '''
        self.__config = config

    def __run_solution(self, solution, test_path):
        ''' Returns output [if invoker says OK] '''
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

        output_path = test_path + ".out"

        if os.path.exists(output_path):
            with open(output_path) as f:
                out = f.read()
            os.remove(output_path)
            return out

        return ""


    def __generate_test(self, generator):
        ''' Creates random test '''
        newrand = random.randint(0, globalconfig.stress_up)
        test_info = cmd_gen_test_info.CmdOrGenTestInfo(generator, [str(newrand)])
        self.logger.warning("Random number for generator is: %s" % newrand)
        # generate ONE random test using given generator
        return TestsGenerator([test_info], "stress").generate(lambda x: True, False)[0]

    def __compare_outputs(self, input, correct_out, second_out, checker):
        ''' Compares two outputs with checker, returns True/False '''
        if not os.path.exists(".please"):
            os.mkdir(".please")
        correct_out_path = os.path.join(self.PLEASE_TEMP, self.CORRECT_OUT)
        with open(correct_out_path, "w") as f:
            f.write(correct_out)

        second_out_path = os.path.join(self.PLEASE_TEMP, self.INCORRECT_OUT)
        with open(second_out_path, "w") as f:
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
                    raise PleaseException("Test failed")
                except StressCheckFail:
                    raise PleaseException("Check failed")
                finally:
                    if os.path.exists(test_path):
                        os.remove(test_path)
                    if os.path.exists(test_path + globalconfig.temp_solution_out_file):
                        os.remove(test_path + globalconfig.temp_solution_out_file)
        except KeyboardInterrupt:
            self.logger.info("Interrupted")
