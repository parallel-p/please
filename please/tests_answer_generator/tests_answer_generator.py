from ..test_config_parser import parser
import io
import os
from please import globalconfig
from ..tests_generator import tests_generator
from ..invoker.invoker import ExecutionLimits
from ..validator_runner import validator_runner
from ..answers_generator import answers_generator
from ..solution_tester import package_config
import logging
from ..utils import utests
from ..well_done import well_done
from please.log import logger
from ..utils import form_error_output

class ValidatorError(Exception):
    pass

def get_file_name(testinfo):
    return testinfo

def get_return_code (validators_result):
    return validators_result[0].return_code

def get_verdict (validators_result):
    return validators_result[0].verdict

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
        count_errors = 0
        tests = tests or utests.get_tests()
        if 'validator' in config and config['validator'] not in ["", None]:
            for num, test_filename in enumerate(tests):
                logger.info("Start validator on test #" + str(num+1))
                validator_result = validator_runner.validate(config["validator"], test_filename)
                if get_return_code(validator_result) != 0:
                    count_errors += 1
                verd = get_verdict(validator_result)
                if verd == "FNF":
                    raise ValidatorError("Validator isn't found")
                if verd == "OK":
                    logger.info("Validator said OK")
                else:
                    err_out = form_error_output.process_err_exit("Validator executions has had", verd, validator_result[0].return_code,
                                                       validator_result[1].decode(), validator_result[2].decode())
                    raise ValidatorError(err_out)
        else:
            logger.warning("Validator is empty")

    def __get_admit (self, tags):
        def admit(attr):
            for tag in tags:
                if not tag in attr:
                    return False
            return True

        return admit

    def __generate_answers (self, tests):
        self.validate(tests)
        config = package_config.PackageConfig.get_config()
        # TODO: check if config is None
        return answers_generator.AnswersGenerator().generate(tests, config["main_solution"], [], config)
    
    def generate_all(self):
        tests = tests_generator.TestsGenerator(parser.FileTestConfigParser(self.__create_well_done("well_done_test") ).get_test_info_objects()).generate_all()
        answers = self.__generate_answers(tests)
        return zip(tests, answers)
        
    def generate (self,tags, prefix = "", delete_folder=True):
        tests = tests_generator.TestsGenerator(parser.FileTestConfigParser(self.__create_well_done("well_done_test")  ).get_test_info_objects(), prefix).generate( self.__get_admit ( tags ), delete_folder )
        answers = self.__generate_answers(tests)
        return zip(tests, answers)
    
    def __create_well_done(self, key):
        # TODO: check if config returned by package_config.PackageConfig.get_config is None
        return well_done.WellDone(package_config.PackageConfig.get_config()[key])

