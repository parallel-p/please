import os

from django.shortcuts import render_to_response
from django.template import RequestContext

import please.globalconfig
from please.reports.generate_html_report import get_test_results_from_solution

from problem.models import Problem, Solution, Verdict, TestResult
from problem.forms import SolutionAddForm, EmptyForm
from problem.views.file_utils import file_save
from problem.views.file_utils import ChangeDir
from problem.synchronization import export_from_database


def retest_solutions(request, id):
    problem = Problem.objects.get(id=id)
    solutions = [{'obj': solution,
                  'path': solution.path,
                  'name': os.path.relpath(solution.path, please.globalconfig.solutions_dir),
                  'expected_verdicts': solution.expected_verdicts.all(),
                  'possible_verdicts': solution.possible_verdicts.all()} for solution in Solution.objects.filter(problem__id=id)]

    if request.method == 'POST':
        form = EmptyForm(request.POST)
        print(form.data)
        for solution in solutions:
            if (solution['name'] + '_retest' in form.data) or ("retest_all_solutions" in form.data):
                for i in TestResult.objects.filter(solution=solution['obj']):
                    i.delete()
                with ChangeDir(problem.path):
                    results = get_test_results_from_solution(solution['path'])[2]
                    results = sorted(results.items(), key=lambda x: int(os.path.basename(x[0])))
                    for result in results:
                        test_result = TestResult(solution=solution['obj'],
                                                 verdict=result[1][0].verdict,
                                                 return_code=result[1][0].return_code,
                                                 real_time=result[1][0].real_time,
                                                 cpu_time=result[1][0].cpu_time,
                                                 used_memory=result[1][0].used_memory,
                                                 test_number=int(os.path.basename(result[0])),
                                                 checker_stdout=result[1][1],
                                                 checker_stderr=result[1][2])
                        test_result.save()
    output = []
    max_count = 0

    for solution in solutions:
        output.append([{'verdict': str(results.verdict),
                        'time': str(results.cpu_time),
                        'solution': solution['name']} for results in TestResult.objects.filter(solution=solution['obj'])])
        max_count = max(max_count, len(output[-1]))

    for row in output:
        if len(i) != max_count:
            row.extend([{}] * (max_count - len(i)))
    return {'output': list(zip(*(output))),
            'solutions': [solution['name'] for solution in solutions],
            'expected_verdicts': [solution['expected_verdicts'] for solution in solutions],
            'possible_verdicts': [solution['possible_verdicts'] for solution in solutions]}


def upload_solution(request, id):
    problem = Problem.objects.get(id=id)
    if request.method == 'POST':
        form = SolutionAddForm(request.POST, request.FILES)
        if 'submit_file' in form.data:
            if form.is_valid() and request.FILES:
                solution = Solution(problem=problem)
                directory = os.path.join(str(problem.path), 'solutions')
                solution.path = os.path.relpath(
                        file_save(request.FILES['solution_file'], directory),
                        start=str(problem.path))
                solution.input = form.cleaned_data['input_file_name']
                solution.output = form.cleaned_data['output_file_name']
                solution.save()
                for choice in Verdict.objects.filter(name__in=form.cleaned_data['possible_verdicts']):
                    solution.possible_verdicts.add(choice)
                for choice in Verdict.objects.filter(name__in=form.cleaned_data['expected_verdicts']):
                    solution.expected_verdicts.add(choice)
                solution.save()
                form = SolutionAddForm()
                export_from_database(problem)
        else:
            form = SolutionAddForm()
    else:
        form = SolutionAddForm()
    return {'form': form}


def view_solutions(request, id):
    return render_to_response('add_solution.html',
                              upload_solution(request, id),
                              context_instance=RequestContext(request))
