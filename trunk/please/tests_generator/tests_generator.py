import shutil
import os
from ..utils import line_ending
from ..executors import compiler, runner
from .. import globalconfig
from ..package import package_config
import io
import logging
from please import test_info

logger = logging.getLogger('please_logger.TestsGenerator')

TESTS_DIR = globalconfig.temp_tests_dir

class TestsGenerator:
    def __init__(self, tests_info, prefix=""):
        self.__tests_info = tests_info
        self.__prefix = prefix
        self.config = package_config.PackageConfig.get_config() or dict()
        self.hand_answer_extension = self.config.get('hand_answer_extension', 'a')
    
    def __copy_handfiles(self, testfile, file_name):
        basename = os.path.splitext(testfile.desc)[0]
        hand_ansfile = basename + '.' + self.hand_answer_extension
        if os.path.exists(hand_ansfile):
            shutil.copy(hand_ansfile, file_name + '.ha')
            logger.info("    Hand answer file '%s'" % hand_ansfile)

        tex_testfile = basename + '.tex'
        if os.path.exists(tex_testfile):
            shutil.copy(tex_testfile, file_name + '.tex')
            logger.info("    Tex test '%s'" % tex_testfile)

        tex_ansfile = basename + '.a.tex'
        if os.path.exists(tex_ansfile):
            shutil.copy(tex_ansfile, file_name + '.a.tex')
            logger.info("    Tex answer '%s'" % tex_ansfile)

    def __generate_test(self, test, first_test_id):
        test_files = test.tests()
        file_names = []
        num = first_test_id
        for testfile in test_files:
            num += 1
            file_name = self.__prefix + "{0:d}".format(num)
            file_name = os.path.join(TESTS_DIR, file_name)     
            testfile.write(file_name)
            file_names.append(file_name)
            line_ending.convert(file_name)
            logger.info("Test #%d '%s' is generated" % (num, testfile.desc))

            if type(testfile) == test_info.test_file.FileTestFile:
                self.__copy_handfiles(testfile, file_name)
        return file_names, num - first_test_id
    
    def generate(self, admit, delete_folder=True):
        '''
        generates tests, whos tags admit given lambda
        '''        
        if delete_folder:
            if os.path.exists(TESTS_DIR):
                shutil.rmtree(os.path.join(TESTS_DIR))        
        if not os.path.exists(TESTS_DIR):
            os.makedirs(TESTS_DIR)
        generated = []
        given = [test for test in self.__tests_info if admit(test.get_tags())]
        logger.info('Generating {0} tests series:\n'.format(len(given)))
        
        current_test_id = 0
        for i, test in enumerate(given):
            # TODO: this should be changed to generated_tests_count
            file_names, tests_in_series_count = self.__generate_test(test, current_test_id)    
            current_test_id += tests_in_series_count               
            for file_name in file_names:
                generated.append(file_name)
            logger.info('Test series #{0} generated\n'.format(i + 1))
        return generated
        
    def generate_all(self):
        return self.generate(lambda x: True)
