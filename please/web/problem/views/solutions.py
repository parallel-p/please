from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
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
            solution.input = file_save(request.FILES['input_file'], dir)
            solution.output = file_save(request.FILES['output_file'], dir)
            solution.save()
            for choice in filter(
                    lambda t: t[0] in form.cleaned_data['expected_verdicts'],
                    form.fields['expected_verdicts'].choices):
                solution.expected_verdicts.add(choice.id)
            for choice in filter(
                    lambda t: t[0] in form.cleaned_data['possible_verdicts'],
                    form.fields['possible_verdicts'].choices):
                solution.possible_verdicts.add(choice.id)
            solution.save()
            form = SolutionAddForm()
    else:
        form = SolutionAddForm()
    return {'problem_solution_add': {'form' : form}, 'problem_id': problem_id}

def add(request, problem_id):
    return render_to_response('add_solution.html',
        add_block(request, problem_id),
        context_instance=RequestContext(request))
