from .. import globalconfig
from ..test_config_parser import parser
from ..language_configurator.lang_conf import get_language_configurator
from ..solution_tester import package_config
import os
import shutil
from ..executors import trash_remover
import logging

logger = logging.getLogger("please_logger.cleaner.cleaner")

class Cleaner:
    def __clean_binary(self, source):
        lang_conf = get_language_configurator(source)
        if lang_conf is not None:
            binary_name = lang_conf.get_binary_name(source)[0]
            if os.path.exists(binary_name):
                logger.info("Removing " + binary_name)
                os.remove(binary_name)
            else:
                logger.info("There is no binary file for " + source)
                
    def cleanup(self):
        if os.path.exists(globalconfig.temp_statements_dir):
            shutil.rmtree(globalconfig.temp_statements_dir)
        if os.path.exists(globalconfig.temp_tests_dir):
            shutil.rmtree(globalconfig.temp_tests_dir)
        config = package_config.PackageConfig.get_config()
        self.__clean_binary(config["validator"])
        self.__clean_binary(config["checker"])
        self.__clean_binary(config["main_solution"])
        self.__clean_binary(config["description"])
        self.__clean_binary(config["statement"])
        solutions = config["solution"]
        if solutions != None:
            for solution in solutions:    
                self.__clean_binary(solution["source"])
        tests = parser.parse_test_config()
        generators = []
        for test in tests:
            if test.type == parser.TestInfoType.GENERATOR and test.command[0] not in generators:
                self.__clean_binary(test.command[0])
                generators.append(test.command[0])
        trash_remover.remove_logs_in_depth(globalconfig.logs, ".")