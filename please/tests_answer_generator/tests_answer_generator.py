from ..test_config_parser import parser
import io
import os
from please import globalconfig
from ..tests_generator import tests_generator
from ..invoker.invoker import ExecutionLimits
from ..validator_runner import validator_runner
from ..answers_generator import answers_generator
from ..package import package_config
from ..executors import runner
import logging
from ..utils import utests
from ..utils.exceptions import PleaseException
from ..well_done import well_done
from please.log import logger
from ..utils import form_error_output

class WellDoneWithValidator:
    def __init__(self, validator = None, well_done = None):
        self.__validator = validator
        self.__well_done = well_done

    def validate(self, test_filename, test_num):
        logger.info("Start validator on test #%d" % test_num)
        if self.__well_done:
            outcome, errors = self.__well_done.check(test_filename, fix_inplace=False)
            if outcome != well_done.OK:
                raise PleaseException("Well done test failed on %s" % " ".join(errors))
        if self.__validator:
            invoke_info, stdout, stderr = validator_runner.validate(
                    self.__validator, test_filename)
            if invoke_info.verdict == "FNF":
                raise PleaseException("Validator %s not found" % validator_src)
            if invoke_info.verdict == "OK":
                logger.info("Validator said OK")
            else:
                raise PleaseException(
                    form_error_output.process_err_exit(
                        "Validator has crashed",
                        invoke_info.verdict,
                        invoke_info.return_code,
                        stdout,
                        stderr))

class TestsAndAnswersGenerator:
    """
    function generate_all() generates all the tests of file tests.please
    function generate(tags) generates tests with tags
    tags - list of tags
    Example:
     TestsAndAnswersGenerator().generate(["BIG_TESTS"])
    """
    def validate(self, tests=None):
        config = package_config.PackageConfig.get_config()
        # TODO: check if config is None
        well_test = self.__create_well_done("well_done_test")

        if tests is None:
            tests = utests.get_tests()
        if 'validator' in config and config['validator'] not in ["", None]:
            validator_src = config["validator"]
        else:
            validator_src = None
            logger.warning("Validator is empty")

        well_done_with_validator = WellDoneWithValidator(
                validator=validator_src, well_done=well_test)
        for num, test in enumerate(tests):
            well_done_with_validator.validate(test, num+1)

    def __get_admit (self, tags):
        class Admit:
            def __init__(self, tags):
                self.tags = tags
            def __call__(self, attr):
                for tag in self.tags:
                    if not tag in attr:
                        return False
                return True

        return Admit(tags)

    def __generate_answers (self, tests):
        self.validate(tests)
        config = package_config.PackageConfig.get_config()
        # TODO: check if config is None
        return answers_generator.AnswersGenerator().generate(tests, config["main_solution"], [], config)
    
    def generate_all(self):
        tests = tests_generator.TestsGenerator(
                parser.FileTestConfigParser(self.__create_well_done("well_done_test")
                ).get_test_info_objects()
            ).generate_all()
        answers = self.__generate_answers(tests)
        return zip(tests, answers)
        
    def generate (self,tags, prefix = "", delete_folder=True):
        tests = tests_generator.TestsGenerator(
                parser.FileTestConfigParser(
                    self.__create_well_done("well_done_test")
                ).get_test_info_objects(), prefix).generate(
                    self.__get_admit ( tags ), delete_folder
                )
        answers = self.__generate_answers(tests)
        return zip(tests, answers)
    
    def __create_well_done(self, key):
        # TODO: check if config returned by package_config.PackageConfig.get_config is None
        return well_done.WellDone(package_config.PackageConfig.get_config()[key])

