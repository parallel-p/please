from please.command_line.word_template import WordTemplate, WordMistake
import unittest

class WordMistakeTest(unittest.TestCase):
    def test_differents(self):
        for a, b, ans in [("abc", "abc", 0),
                          ("abc", "abs", 1),
                          ("qwe", "ewq", 2)]:
            self.assertEqual(WordMistake.differents(a, b), ans)

    def test_one_change_letter(self):
        for a, b, ans in [("abc", "abc", True),
                          ("abc", "abs", True),
                          ("qwe", "ewq", False),
                          ("abc", "acb", False),
                          ("abc", "abcd", False)]:
            self.assertEqual(WordMistake.one_change_letter(a, b), ans)

    def test_one_add_letter(self):
        for a, b, ans in [("abc", "dabc", True),
                          ("abc", "abdc", True),
                          ("abc", "abs", False),
                          ("qwe", "ewq", False),
                          ("abc", "acb", False)]:
            self.assertEqual(WordMistake.one_add_letter(a, b), ans)

    def test_one_del_letter(self):
        for a, b, ans in [("dabc", "abc", True),
                          ("abdc", "abc", True),
                          ("abs", "abc", False),
                          ("ewq", "qwe", False),
                          ("acb", "abc", False)]:
            self.assertEqual(WordMistake.one_del_letter(a, b), ans)

    def test_one_swap_letter(self):
        for a, b, ans in [("abc", "bac", True),
                          ("abdc", "adbc", True),
                          ("abc", "abc", False),
                          ("ewq", "qwe", False),
                          ("acb", "abc", True)]:
            self.assertEqual(WordMistake.one_swap_letter(a, b), ans)

class WordTemplateTest(unittest.TestCase):
    def test_corresponds(self):
        template = "solution|sol|so"
        command_list = template.split("|")
        word_template = WordTemplate(template)
        for command in command_list :
            self.assertTrue(word_template.corresponds(command))

        template = "create|creat|cr"
        word_template = WordTemplate(template)
        self.assertTrue(word_template.corresponds("cr"))

        template = "create"
        command_list = template.split("|")
        word_template = WordTemplate(template)
        for i in command_list:
            self.assertTrue(word_template.corresponds(i))

        template = "add|ad"
        word_template = WordTemplate(template)
        self.assertTrue(word_template.corresponds("add"))

    def test_mistake_corresponds (self) :
        #different symbol mistake
        template = "solution|sol|so"
        word_template = WordTemplate(template)
        self.assertTrue(word_template.mistake_corresponds("solption"))
        self.assertTrue(word_template.mistake_corresponds("solutiop"))
        self.assertTrue(word_template.mistake_corresponds("zolution"))

        #swap mistake
        """template = "solution|sol|so"
        word_template = WordTemplate(template)
        self.assertTrue(word_template.mistake_corresponds("soultion"))
        self.assertTrue(word_template.mistake_corresponds("oslution"))
        self.assertTrue(word_template.mistake_corresponds("solutino"))
        print("---")
        """

        #missed symbol mistake
        template = "solution|sol|so"
        word_template = WordTemplate(template)
        self.assertTrue(word_template.mistake_corresponds("soltion"))
        self.assertTrue(word_template.mistake_corresponds("olution"))
        self.assertTrue(word_template.mistake_corresponds("solutio"))
        self.assertTrue(word_template.mistake_corresponds("slution"))

        #added symbol mistake
        template = "solution|sol|so|create"
        word_template = WordTemplate(template)
        self.assertTrue(word_template.mistake_corresponds("soluztion"))
        self.assertTrue(word_template.mistake_corresponds("szolution"))
        self.assertTrue(word_template.mistake_corresponds("zsolution"))
        self.assertTrue(word_template.mistake_corresponds("creates"))
        self.assertTrue(word_template.mistake_corresponds("sols"))

        #if the word isn't rightit works
        template = "solution|sol|so"
        word_template = WordTemplate(template)

        self.assertFalse(word_template.mistake_corresponds("oslutiop"))

        #if the word isn't right

        template = "solution|create|add|megalongword|problem|gets|task"
        word_template = WordTemplate(template)
        self.assertTrue(word_template.mistake_corresponds("ad"))
        self.assertTrue(word_template.mistake_corresponds("adb"))
        self.assertFalse(word_template.mistake_corresponds("adddddddd"))
        self.assertTrue(word_template.mistake_corresponds("tasc"))
        self.assertTrue(word_template.mistake_corresponds("get"))
        self.assertFalse(word_template.mistake_corresponds("soluti"))
        self.assertTrue(word_template.mistake_corresponds("creat"))
        self.assertFalse(word_template.mistake_corresponds("abb"))
        self.assertFalse(word_template.mistake_corresponds("megalongwo"))
        self.assertFalse(word_template.mistake_corresponds("ssprbolem"))

        #the  corresponds take it
        template = "solution"
        word_template = WordTemplate(template)
        self.assertTrue(word_template.mistake_corresponds("solution"))

        #if there is no word in template (with mistake)
        template = "get"
        word_template = WordTemplate (template)
        self.assertFalse(word_template.mistake_corresponds("Do"))

if __name__ == '__main__':
    unittest.main()
