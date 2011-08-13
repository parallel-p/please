import shutil
import os
from please.executors import compiler, runner
from please.utils import line_ending
from .. import globalconfig
import io
import logging

logger = logging.getLogger('please_logger.TestsGenerator')

TESTS_DIR = globalconfig.temp_tests_dir

class TestsGenerator:
    def __init__(self, tests_info):
        self.__tests_info = tests_info
    
    def __generate_test(self, test, test_id):
        
        file_name = "{0:d}".format(test_id)
        file_name = os.path.join(TESTS_DIR, file_name)
        if (test.type == 'file'):
            shutil.copyfile(test.command, file_name)
        elif (test.type == 'command'):
            f = io.open(file_name, 'wb')
            with f:
                res = runner.run(test.command[0], test.command[1], shell = True)[1]
                f.write(res)
        elif (test.type == 'generator'):
            compiler.compile(test.command[0])
            f = io.open(file_name, 'wb')
            with f:
                res = runner.run(test.command[0], test.command[1])[1]
                f.write(res)
            
        line_ending.convert(file_name)
        return file_name
    def generate(self, admit):
        '''
        generates tests, whos tags admit given lambda
        '''
        if not os.path.exists(TESTS_DIR):
            os.makedirs(TESTS_DIR)
        generated = []
        
        logger.info('Generating {0} tests'.format(len([test for test in self.__tests_info if admit(test.attributes)])))
        
        for i, test in enumerate(self.__tests_info):
            if (admit(test.attributes)):
                file_name = self.__generate_test(test, i + 1)
                generated.append(file_name)
                logger.info('Test #{0} generated'.format(i + 1))
        
        return generated
        
    def generate_all(self):
        if (os.path.exists(TESTS_DIR)):
            shutil.rmtree(os.path.join(TESTS_DIR))
        return self.generate(lambda x: True)
