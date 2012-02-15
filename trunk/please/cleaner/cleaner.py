from .. import globalconfig
from ..lang_config import get_lang_config
from ..solution_tester import package_config
import os
import shutil
from ..executors import trash_remover
import logging
from ..test_config_parser import parser

logger = logging.getLogger("please_logger.cleaner.cleaner")

class Cleaner:
    def __clean_binary(self, source):
        if source is not None:
            lang_conf = get_lang_config(source)
            if lang_conf is not None:
                binaries = lang_conf._get_binaries(source)
                for binary in binaries:
                    if os.path.exists(binary):
                        logger.info("Removing " + binary)
                        os.remove(binary)
                    else:
                        logger.info("There is no binary file for " + source)
                
    def cleanup(self):
        if os.path.exists(globalconfig.temp_statements_dir):
            shutil.rmtree(globalconfig.temp_statements_dir)
        if os.path.exists(globalconfig.temp_tests_dir):
            shutil.rmtree(globalconfig.temp_tests_dir)
        config = package_config.PackageConfig.get_config()
        # TODO: check if config is None
        self.__clean_binary(config["validator"])
        self.__clean_binary(config["checker"])
        self.__clean_binary(config["main_solution"])
        self.__clean_binary(config["description"])
        self.__clean_binary(config["statement"])
        solutions = config["solution"]
        if solutions != None:
            for solution in solutions:
                self.__clean_binary(solution["source"])
        generators = parser.FileTestConfigParser().get_binaries()
        for generator in generators:
            self.__clean_binary(generator)
        if os.path.exists("report.html"):
            logger.info("Removing report.html")
            os.remove("report.html")
        else:
            logger.info("There is no report.html")
        trash_remover.remove_logs_in_depth()

