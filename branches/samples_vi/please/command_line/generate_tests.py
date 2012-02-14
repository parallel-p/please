from ..tests_answer_generator.tests_answer_generator import TestsAndAnswersGenerator

test_generator = TestsAndAnswersGenerator()

def generate_tests_with_tags(tags):
    test_generator.generate(tags)

def generate_tests():
    test_generator.generate_all()						
