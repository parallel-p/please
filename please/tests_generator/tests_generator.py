import shutil
import os
from ..executors import compiler, runner
from ..utils import line_ending
from .. import globalconfig
import io
import logging

logger = logging.getLogger('please_logger.TestsGenerator')

TESTS_DIR = globalconfig.temp_tests_dir

class TestsGenerator:
    def __init__(self, tests_info, prefix=""):
        self.__tests_info = tests_info
        self.__prefix = prefix
        
    def generate(self, admit):
        '''
        generates tests, whos tags admit given lambda
        '''
        if not os.path.exists(TESTS_DIR):
            os.makedirs(TESTS_DIR)
        generated = []
        
        logger.info('Generating {0} tests'.format(len([test for test in self.__tests_info if admit(test.get_tags())])))
        global_test_counter = 1
        
        for test in self.__tests_info:
            if (admit(test.get_tags())):
                files = test.tests()
                for file in files:
                    new_file_name = self.__prefix + "{0:d}".format(global_test_counter)
                    new_file_name = os.path.join(TESTS_DIR, new_file_name)
                    shutil.move(file, new_file_name)
                    #As TestInfo descendants give to us temporary files with tests, we should move 'em
                    global_test_counter += 1
                    generated.append(new_file_name)
                    logger.info('Test #{0} generated'.format(global_test_counter))
        
        return generated
        
    def generate_all(self):
        if (os.path.exists(TESTS_DIR)):
            shutil.rmtree(os.path.join(TESTS_DIR))
        return self.generate(lambda x: True)
