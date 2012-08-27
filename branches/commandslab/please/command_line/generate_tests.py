from ..tests_answer_generator import generate, generate_all, AdmitAny, AdmitAll

def generate_tests_with_tags(tags):
    stags = ' '.join(tags)
    if ',' in tags:
        tags = [x.strip() for x in stags.split(',')]
        admit = AdmitAny
    else:
        admit = AdmitAll
    generate(tags, admit=admit)

def generate_tests():
    generate_all()						
