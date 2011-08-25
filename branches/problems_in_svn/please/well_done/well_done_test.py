from filecmp import cmp
from shutil import copyfile, rmtree
from os import remove
import os.path
import mox
import logging

import unittest
from please.well_done.well_done import *

class Tester(unittest.TestCase):

    __dir = os.path.dirname(__file__)

    def __tests_runner(self,filename, func_list, correct_result):
        copyfile(os.path.join(self.__dir, 'testdata', filename), 
                os.path.join(self.__dir, 'tmp'))
        self.assertEqual(WellDone(os.path.join(self.__dir, 'tmp'), func_list).check(), correct_result)
        #Uncomment the followin line to leave fixed files as *.b files in testdata
        #copyfile(os.path.join(self.__dir, 'tmp'), os.path.join(self.__dir, 'testdata', filename + '.b'))
        self.assertTrue(cmp(os.path.join(self.__dir, 'tmp'), 
                        os.path.join(self.__dir, 'testdata', filename + '.a')))  

    def test_endswith_EOLN(self):
        self.__tests_runner('1', ['endswith_EOLN'],(OK, []))
        self.__tests_runner('2', ['endswith_EOLN'],(OK, []))
        self.__tests_runner('3', ['endswith_EOLN'],(FIXED, ['endswith_EOLN']))
        self.__tests_runner('4', ['endswith_EOLN'],(FIXED, ['endswith_EOLN']))
        self.__tests_runner('5', ['endswith_EOLN'],(OK, []))
        with self.assertRaises(IOError):
            WellDone(os.path.join(self.__dir, 'tmp2'), ['endswith_EOLN'])

    def test_no_left_spaces(self):
        self.__tests_runner('106', ['no_left_space'],(OK, []))
        self.__tests_runner('107', ['no_left_space'],(OK, []))
        self.__tests_runner('108', ['no_left_space'],(OK, []))
        self.__tests_runner('109', ['no_left_space'],(OK, []))
        self.__tests_runner('110', ['no_left_space'],(FIXED, ['no_left_space']))
        self.__tests_runner('111', ['no_left_space'],(OK, []))
        self.__tests_runner('112', ['no_left_space'],(FIXED, ['no_left_space']))
        self.__tests_runner('113', ['no_left_space'],(FIXED, ['no_left_space']))
        self.__tests_runner('114', ['no_left_space'],(OK, []))
        self.__tests_runner('115', ['no_left_space'],(FIXED, ['no_left_space']))
        self.__tests_runner('116', ['no_left_space'],(OK, []))
        self.__tests_runner('117', ['no_left_space'],(OK, []))
        self.__tests_runner('118', ['no_left_space'],(FIXED, ['no_left_space']))
        self.__tests_runner('119', ['no_left_space'],(FIXED, ['no_left_space']))
        
    def test_no_right_spaces(self):
        self.__tests_runner('206', ['no_right_space'],(OK, []))
        self.__tests_runner('207', ['no_right_space'],(OK, []))
        self.__tests_runner('208', ['no_right_space'],(OK, []))
        self.__tests_runner('209', ['no_right_space'],(OK, []))
        self.__tests_runner('210', ['no_right_space'],(OK, []))
        self.__tests_runner('211', ['no_right_space'],(FIXED, ['no_right_space']))
        self.__tests_runner('212', ['no_right_space'],(FIXED, ['no_right_space']))
        self.__tests_runner('213', ['no_right_space'],(OK, []))
        self.__tests_runner('214', ['no_right_space'],(FIXED, ['no_right_space']))
        self.__tests_runner('215', ['no_right_space'],(FIXED, ['no_right_space']))
        self.__tests_runner('216', ['no_right_space'],(OK, []))
        self.__tests_runner('217', ['no_right_space'],(OK, []))
        self.__tests_runner('218', ['no_right_space'],(FIXED, ['no_right_space']))
        self.__tests_runner('219', ['no_right_space'],(FIXED, ['no_right_space']))
        
    def test_no_left_right_spaces(self):
        self.__tests_runner('6', ['no_left_right_space'],(OK, []))
        self.__tests_runner('7', ['no_left_right_space'],(OK, []))
        self.__tests_runner('8', ['no_left_right_space'],(OK, []))
        self.__tests_runner('9', ['no_left_right_space'],(OK, []))
        self.__tests_runner('10', ['no_left_right_space'],(FIXED, ['no_left_right_space']))
        self.__tests_runner('11', ['no_left_right_space'],(FIXED, ['no_left_right_space']))
        self.__tests_runner('12', ['no_left_right_space'],(FIXED, ['no_left_right_space']))
        self.__tests_runner('13', ['no_left_right_space'],(FIXED, ['no_left_right_space']))
        self.__tests_runner('14', ['no_left_right_space'],(FIXED, ['no_left_right_space']))
        self.__tests_runner('15', ['no_left_right_space'],(FIXED, ['no_left_right_space']))
        self.__tests_runner('16', ['no_left_right_space'],(OK, []))
        self.__tests_runner('17', ['no_left_right_space'],(OK, []))
        self.__tests_runner('18', ['no_left_right_space'],(FIXED, ['no_left_right_space']))
        self.__tests_runner('19', ['no_left_right_space'],(FIXED, ['no_left_right_space']))
        
    def test_no_symbols_less_32(self): 
        self.__tests_runner('20', ['no_symbols_less_32'],(CRASH, ['no_symbols_less_32']))
        self.__tests_runner('21', ['no_symbols_less_32'],(CRASH, ['no_symbols_less_32']))
        self.__tests_runner('22', ['no_symbols_less_32'],(CRASH, ['no_symbols_less_32']))
        self.__tests_runner('23', ['no_symbols_less_32'],(OK, []))
        
    def test_no_double_space(self):
        self.__tests_runner('30', ['no_double_space'],(OK, []))
        self.__tests_runner('28', ['no_double_space'],(FIXED, ['no_double_space']))
        self.__tests_runner('29', ['no_double_space'],(FIXED, ['no_double_space']))
 
    def test_no_top_emptyline(self):
        self.__tests_runner('131', ['no_top_emptyline'],(OK, []))
        self.__tests_runner('132', ['no_top_emptyline'],(OK, []))
        self.__tests_runner('133', ['no_top_emptyline'],(FIXED, ['no_top_emptyline']))
        self.__tests_runner('134', ['no_top_emptyline'],(FIXED, ['no_top_emptyline']))
        self.__tests_runner('135', ['no_top_emptyline'],(OK, []))
        self.__tests_runner('136', ['no_top_emptyline'],(FIXED, ['no_top_emptyline']))
    
    def test_no_bottom_emptyline(self):
        self.__tests_runner('231', ['no_bottom_emptyline'],(OK, []))
        self.__tests_runner('232', ['no_bottom_emptyline'],(OK, []))
        self.__tests_runner('233', ['no_bottom_emptyline'],(OK, []))
        self.__tests_runner('234', ['no_bottom_emptyline'],(OK, []))
        self.__tests_runner('235', ['no_bottom_emptyline'],(FIXED, ['no_bottom_emptyline']))
        self.__tests_runner('236', ['no_bottom_emptyline'],(FIXED, ['no_bottom_emptyline']))
    
    def test_no_top_bottom_emptyline(self):
        self.__tests_runner('31', ['no_top_bottom_emptyline'],(OK, []))
        self.__tests_runner('32', ['no_top_bottom_emptyline'],(OK, []))
        self.__tests_runner('33', ['no_top_bottom_emptyline'],(FIXED, ['no_top_bottom_emptyline']))
        self.__tests_runner('34', ['no_top_bottom_emptyline'],(FIXED, ['no_top_bottom_emptyline']))
        self.__tests_runner('35', ['no_top_bottom_emptyline'],(FIXED, ['no_top_bottom_emptyline']))
        self.__tests_runner('36', ['no_top_bottom_emptyline'],(FIXED, ['no_top_bottom_emptyline']))
    
    def test_not_empty(self):
        self.__tests_runner('24', ['not_empty'],(CRASH, ['not_empty']))
        self.__tests_runner('25', ['not_empty'],(CRASH, ['not_empty']))
        self.__tests_runner('26', ['not_empty'],(OK, []))
        self.__tests_runner('27', ['not_empty'],(CRASH, ['not_empty']))
 
    def test_no_emptyline(self):
        self.__tests_runner('42', ['no_emptyline'],(OK, []))
        self.__tests_runner('43', ['no_emptyline'],(OK, []))
        self.__tests_runner('44', ['no_emptyline'],(FIXED, ['no_emptyline']))
        self.__tests_runner('45', ['no_emptyline'],(FIXED, ['no_emptyline']))
        self.__tests_runner('46', ['no_emptyline'],(FIXED, ['no_emptyline']))
        self.__tests_runner('47', ['no_emptyline'],(FIXED, ['no_emptyline']))
        self.__tests_runner('48', ['no_emptyline'],(FIXED, ['no_emptyline']))

    def test_complex(self):
        self.__tests_runner('37', ['endswith_EOLN', 'no_symbols_less_32', 
                 'no_right_space', 'no_double_space', 
                 'no_bottom_emptyline', 'not_empty'],(OK, []))
        self.__tests_runner('38', ['no_symbols_less_32', 
                 'no_left_right_space', 'no_double_space', 
                 'no_top_emptyline', 'endswith_EOLN', 'not_empty'], 
                 (FIXED, ['no_left_right_space', 
                   'no_double_space', 'no_top_emptyline']))
        self.__tests_runner('39', ['no_symbols_less_32', 
                 'no_right_space', 'no_double_space', 
                 'no_emptyline', 'endswith_EOLN', 'not_empty'], 
                 (CRASH, ['not_empty']))
        self.__tests_runner('40', ['no_symbols_less_32', 
                 'no_left_right_space', 'no_double_space', 
                 'no_top_bottom_emptyline', 'endswith_EOLN'], 
                 (FIXED, ['no_left_right_space', 'no_top_bottom_emptyline', 
                  'endswith_EOLN']))
        self.__tests_runner('41', [], (OK, []))
        with self.assertRaises(AttributeError):
            self.__tests_runner('41', ['no_symbols_less_32', 
                 'no_left_right_space', 'no_such_function', 
                 'no_top_bottom_emptyline', 'endswith_EOLN'], 
                 (FIXED, ['no_left_right_space', 'no_top_bottom_emptyline', 
                  'endswith_EOLN']))

    #def __tests_check_runner(self, filename, func_list, correct_result):
    #    copyfile(os.path.join(self.__dir, 'testdata', filename), 
    #            os.path.join(self.__dir, 'tmp'))
    #    self.assertEqual(WellDone(os.path.join(self.__dir, 'tmp'), func_list).check(), correct_result)
    #    copyfile(os.path.join(self.__dir, 'tmp'), os.path.join(self.__dir, 'testdata', filename + '.b'))
    #    self.assertTrue(cmp(os.path.join(self.__dir, 'tmp'), 
    #                    os.path.join(self.__dir, 'testdata', filename + '.a')))  

    def setUp(self):
        self.mox = mox.Mox()


    def __well_done_check_runner(self, filename, function_list, log):
        self.mox.StubOutWithMock(logging, "getLogger")
        logger = self.mox.CreateMockAnything()
        logger.info(log)
        logging.getLogger("please_logger.well_done").AndReturn(logger)
        self.mox.ReplayAll()
        os.mkdir(os.path.join(self.__dir,'.tests'))
        copyfile(os.path.join(self.__dir, 'testdata', filename), os.path.join(self.__dir, filename))
        well_done_check_test(os.path.join(self.__dir, filename), function_list)
        #copyfile(os.path.join(self.__dir, '.tests', filename), os.path.join(self.__dir, 'testdata', filename + '.b'))
        self.assertTrue(cmp(os.path.join(self.__dir, filename), 
                        os.path.join(self.__dir, 'testdata', filename+'.a')))  
        self.mox.VerifyAll()        
        self.mox.UnsetStubs()
        rmtree(os.path.join(self.__dir, '.tests'))

    def test_well_done_check_test(self):
        self.__well_done_check_runner('.tests/42', ['no_symbols_less_32', 
                 'no_left_right_space', 'no_double_space', 
                 'no_top_bottom_emptyline', 'endswith_EOLN', 'not_empty'], 
                 'C:\\temp\\_sis2011-jul\\P\\please\\please\\trunk\\please\\well_done\\.tests/42 was fixed with no_left_right_space, no_double_space, no_top_bottom_emptyline')
        self.__well_done_check_runner('.tests/43', [], 
                 'C:\\temp\\_sis2011-jul\\P\\please\\please\\trunk\\please\\well_done\\.tests/43 is well-done')
        self.__well_done_check_runner('.tests/44', ['no_symbols_less_32', 
                 'no_left_right_space', 'no_double_space', 
                 'no_top_bottom_emptyline', 'endswith_EOLN', 'not_empty'], 
                 'C:\\temp\\_sis2011-jul\\P\\please\\please\\trunk\\please\\well_done\\.tests/44 check was crashed while testing with not_empty')
         
    def tearDown(self):        
        if os.path.exists(os.path.join(self.__dir, 'tmp')):
            remove(os.path.join(self.__dir, 'tmp'))
        if os.path.exists(os.path.join(self.__dir, '.tests')):
            rmtree(os.path.join(self.__dir, '.tests'))
        self.mox.UnsetStubs()


if __name__ == "__main__":
    unittest.main()

