from django.shortcuts import render_to_response
from django.template import RequestContext
from problem.models import Problem, Solution
from problem.forms import SolutionAddForm
import os.path
from problem.helpers import problem_sync
from problem.views.file_utils import file_save


@problem_sync(read=True, write=False)
def add_block(request, problem_id):
    if request.method == 'POST':
        form = SolutionAddForm(request.POST, request.FILES)
        if form.is_valid():
            solution = Solution(problem=Problem.objects.get(id=problem_id))
            dir = os.path.join(str(solution.problem.path), 'solutions')
            solution.path = file_save(request.FILES['solution_file'], dir)
            solution.input = form.cleaned_data['input_file_name']
            solution.output = form.cleaned_data['output_file_name']
            solution.save()
            print(form.cleaned_data['expected_verdicts'])
            for choice in filter(
                    lambda t: t[1] in form.cleaned_data['expected_verdicts'],
                    form.fields['expected_verdicts'].choices):
                print(choice)
                solution.expected_verdicts.add(choice[0].id)
            for choice in filter(
                    lambda t: t[1] in form.cleaned_data['possible_verdicts'],
                    form.fields['possible_verdicts'].choices):
                solution.possible_verdicts.add(choice[0].id)
            solution.save()
            form = SolutionAddForm()
    else:
        form = SolutionAddForm()
    return {'problem_solution_add': {'form': form}, 'problem_id': problem_id}


def add(request, id):
    return render_to_response('add_solution.html',
        add_block(request, id),
        context_instance=RequestContext(request))
