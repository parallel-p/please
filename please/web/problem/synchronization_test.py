import unittest
from synchronization import *

class Model:
    pass

class SynchronizationTest(unittest.TestCase):
    def test_import_to_database(self):
        path = 'D:/Programming/svn/trunk/please/testdata/problem1'
        model = Model()
        config = import_to_database(model, path, 'default.package')
        print("Name: ", model.name)
        print("Short name: ", model.short_name)
        print("Type: ", model.type)
        print()

        print("Input: ", model.input)
        print("Output: ", model.output)
        print("Time limit: ", model.time_limit)
        print("Memory limit: ", model.memory_limit)
        print()

        print("Checker: ", model.checker)
        print("Validator: ", model.validator)
        print()                      

        print("Statement: ", model.statement)
        print("Description: ", model.description)
        print()

        print("Hand answer extension: ", model.hand_answer_extension)
        print()

        print("Well done test: ", ", ".join(model.well_done_test))
        print("Well done answer: ", ", ".join(model.well_done_answer))
        print()

        print("Analysis: ", model.analysis)
        print()
    
    def test_import_from_database(self):
        pass
            
if __name__ == "__main__":
    unittest.main()
