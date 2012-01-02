import unittest
from please.command_line.template import Template

class Tester(unittest.TestCase):

        def __tests_runner(self,template,args,right_ans):
                self.assertEqual(
                        Template(template.split()).corresponds(args.split()),
                        right_ans)

        def test_template (self):
                self.__tests_runner("add tag #tag","add tag a",{"tag": "a"})
                self.__tests_runner("add tag @tag","add tag a",{"tag": ["a"]})
                self.__tests_runner("create problem #name", "create", None)
                self.__tests_runner("create problem #name",
                                    "create problem n+m",
                                    {'name': 'n+m'})
                self.__tests_runner("get @types solution",
                                    "get OK TL solution",
                                    {'types': ["OK","TL"]})
                self.__tests_runner("get @types solution",
                                    "Do you speak English?",
                                    None)
                self.__tests_runner("get @types solution",
                                    "get ML TL RT solution",
                                    {'types': ["ML", "TL", "RT"]})
                self.__tests_runner("Do you speak English?",
                                    "Do you speak English?",
                                    {})
                self.__tests_runner("@types",
                                    "Do you speak English?",
                                    {'types':
                                     ["Do", "you", "speak", "English?"]})
                self.__tests_runner("create task|problem #name",
                                    "create problem n+m",
                                    {'name': 'n+m'})
                self.__tests_runner("create task|problem #name",
                                    "create problemm n+m",
                                    {'name': 'n+m'})
                self.__tests_runner("create task|problem #name",
                                    "create problm n+m",
                                    {'name': 'n+m'})
                self.__tests_runner("create task|problem #name",
                                    "create prbolem n+m",
                                    {'name': 'n+m'})
                self.__tests_runner("create task|problem #name",
                                    "create tasc n+m",
                                    {'name': 'n+m'})
                self.__tests_runner("create task|problem @name",
                                    "create tasc n+m",
                                    {'name': ['n+m']})
                self.__tests_runner("create task|problem @name",
                                    "create tasc n+m a+b",
                                    {'name': ['n+m', 'a+b']})
                self.__tests_runner("create task|problem @name hello",
                                    "create tasc n+m a+b hello",
                                    {'name': ['n+m', 'a+b']})
                self.__tests_runner("create task|problem #bred @name hello",
                                    "create task abc n+m a+b hello",
                                    {'name': ['n+m', 'a+b'], 'bred' : 'abc'})
                self.__tests_runner("create task|problem #bred @name hello @abc",
                                    "create task abc n+m a+b hello",
                                    None)
                self.__tests_runner("create task|problem @name hello",
                                    "create task hello",
                                    None)

if __name__ == "__main__":
        unittest.main()
