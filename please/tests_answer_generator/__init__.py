from .tests_answer_generator import TestsAndAnswersGenerator
from .tests_answer_generator import AdmitAny, AdmitAll

_tg = TestsAndAnswersGenerator()

generate = _tg.generate
generate_all = _tg.generate_all
validate = _tg.validate
