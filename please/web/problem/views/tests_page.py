import os

from django.shortcuts import render_to_response
import please.globalconfig
from please import answers_generator
from please.utils.exceptions import PleaseException
from problem.models import Problem, TestResult, Solution
from problem.views.file_utils import ChangeDir


def single_test_view(request, id, solution_name, test_id):
    source_path = os.path.join(please.globalconfig.solutions_dir, solution_name)
    problem = Problem.objects.get(id=id)
    solution = Solution.objects.get(problem=problem,
                                    path=source_path)
    results = TestResult.objects.get(solution=solution,
                                     test_number=test_id)
    with ChangeDir(problem.path):
        test_path = os.path.join(please.globalconfig.temp_tests_dir, test_id)
        try:
            answers_generator.generate_answers(tests=[test_path], source_path=source_path)
        except PleaseException as exc:
            full_output = repr(exc)
        else:
            with open(test_path + '.a') as file:
                full_output = file.read()

    return render_to_response('single_test.html',
                              {'full_output': full_output,
                               'results': results})
