import unittest
from synchronization import *

class Model:
    pass

class SynchronizationTest(unittest.TestCase):
    def test_import_to_database(self):
        path = 'D:/Programming/svn/trunk/please/testdata/problem1'
        model = Model()
        config = import_to_database(model, path, 'default.package')
        self.assertLessEqual(len(model.name), 64)
        print("Name: ", model.name)
        self.assertLessEqual(len(model.short_name), 64)
        print("Short name: ", model.short_name)
        self.assertEqual(len(model.type), 0)
        print("Type: ", model.type)
        print()

        self.assertLessEqual(len(model.input), 64)
        print("Input: ", model.input)
        self.assertLessEqual(len(model.output), 64)
        print("Output: ", model.output)
        self.assertLessEqual(float(model.time_limit), 150.0)
        self.assertGreaterEqual(float(model.time_limit), 0.1)
        print("Time limit: ", model.time_limit)
        print("Memory limit: ", model.memory_limit)
        print()

        self.assertLess(len(model.checker), 256)
        print("Checker: ", model.checker)
        self.assertLess(len(model.validator), 256)
        print("Validator: ", model.validator)
        print()                      

        self.assertLess(len(model.statement), 256)
        print("Statement: ", model.statement)
        self.assertLess(len(model.description), 256)
        print("Description: ", model.description)
        print()

        self.assertLess(len(model.hand_answer_extension), 64)
        print("Hand answer extension: ", model.hand_answer_extension)
        print()

        self.assertLessEqual(len(model.validator), 7)
        print("Well done test: ", ", ".join(model.well_done_test))
        self.assertLessEqual(len(model.validator), 7)
        print("Well done answer: ", ", ".join(model.well_done_answer))
        print()

        self.assertLessEqual(len(model.analysis), 256)
        print("Analysis: ", model.analysis)
        print()
    
    def test_import_from_database(self):
        pass
            
if __name__ == "__main__":
    unittest.main()
