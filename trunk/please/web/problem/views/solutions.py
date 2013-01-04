from django.shortcuts import render_to_response
from django.template import RequestContext
from problem.models import Problem, Solution, Verdict
from problem.forms import SolutionAddForm
import os.path
from problem.helpers import problem_sync
from problem.views.file_utils import file_save

def verdicts_with_names(names):
    return filter(lambda verdict: verdict.name in names, Verdict.objects.all())

@problem_sync(read=True, write=False)
def add_block(request, problem_id):
    if request.method == 'POST':
        form = SolutionAddForm(request.POST, request.FILES)
        if form.is_valid():
            solution = Solution(problem=Problem.objects.get(id=problem_id))
            dir = os.path.join(str(solution.problem.path), 'solutions')
            solution.path = os.path.relpath(
                    file_save(request.FILES['solution_file'], dir),
                    start=str(solution.problem.path))
            solution.input = form.cleaned_data['input_file_name']
            solution.output = form.cleaned_data['output_file_name']
            solution.save()
            for choice in verdicts_with_names(
                    form.cleaned_data['possible_verdicts']):
                solution.possible_verdicts.add(choice)
            for choice in verdicts_with_names(
                    form.cleaned_data['expected_verdicts']):
                solution.expected_verdicts.add(choice)
            solution.save()
            form = SolutionAddForm()
    else:
        form = SolutionAddForm()
    return {'problem_solution_add': {'form': form}, 'problem_id': problem_id}


def add(request, id):
    return render_to_response('add_solution.html',
        add_block(request, id),
        context_instance=RequestContext(request))
