import unittest
from please.latex.latex_tools import LatexConstructor, LatexContestConstructor
import os

def read(path):
    with open(path, 'r', encoding = "UTF-8") as read_file:
        content = read_file.read()
        return content

class TestLatexContestConstructor(unittest.TestCase):
    def setUp(self):
        self.__test_dir = os.path.join(os.path.dirname(__file__), 'testdata')
        read_file_dir = os.path.join(self.__test_dir, "contest_template.tex")
        self.__test_object = LatexContestConstructor(read(read_file_dir))
    def test_set_title (self):
        test_title = "Yet another contest"
        self.__test_object.set_title(test_title)
        self.assertEqual(self.__test_object._LatexContestConstructor__attributes["#{contest_title}"], test_title)
    def test_set_date (self):
        test_date = "13 июля, среда"
        self.__test_object.set_date(test_date)
        self.assertEqual(self.__test_object._LatexContestConstructor__attributes["#{contest_date}"], test_date)
    def test_set_location (self):
        test_location = "ЛКШ-2011.июль, Берендеевы Поляны"
        self.__test_object.set_location(test_location)
        self.assertEqual(self.__test_object._LatexContestConstructor__attributes["#{contest_location}"], test_location)

class TestLatexConstructor(unittest.TestCase):
    def setUp(self):
        pass

    def do_test(self, correct, template_problem, input_file, output_file,
                time_limit, memory_limit, title, tests):
        a = LatexConstructor(read(template_problem))

        a.set_input_file(input_file)
        a.set_output_file(output_file)
        a.set_time_limit(time_limit)
        a.set_memory_limit(memory_limit)
        a.set_title(title)
        for test_in, test_out in tests:
            a.add_example(test_in, test_out)

        read_file = open(correct, 'r', encoding = "UTF8")
        correct_ans = read_file.read()
        read_file.close()

        self.assertEqual(a.construct(), correct_ans)

    def test_all(self):
        self.__test_dir = os.path.join(os.path.dirname(__file__), 'testdata')

        test01in = \
"""10
455184306 359222813 948543704 914773487 861885581 253523 770029097 193773919 581789266 457415808
- 1
? 2 5 527021001
? 0 5 490779085
? 0 5 722862778
+ 9 448694272
- 5
? 1 2 285404014
- 4
? 3 4 993634734
+ 0 414639071
"""
        test01out = \
"""1
2
2
0
2
"""
        self.do_test(os.path.join(self.__test_dir, 'problem.in.tex'),
                     os.path.join(self.__test_dir, 'problem.tex'),
                     'kthstat.in', 'kthstat.out', '2 second', '256 MB',
                     'K-th statistics again',
                     [(test01in, test01out)])


if __name__ == "__main__":
    unittest.main()

