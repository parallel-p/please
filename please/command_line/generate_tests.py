from ..tests_answer_generator import generate, generate_all, AdmitAny, AdmitAll

def generate_tests_with_tags(tags):
    generate(tags, admit=AdmitAll)

def generate_tests():
    generate_all()						
