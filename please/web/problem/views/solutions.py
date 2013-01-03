from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from problem.models import Problem, Solution
from problem.forms import SolutionAddForm
import os.path
from problem.helpers import problem_sync


def add_save_file(file, directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)
    fullname = os.path.join(directory, file.name)
    stream = open(fullname, mode='wb')
    stream.write(file.read())
    stream.close()
    return fullname

@problem_sync(read=True, write=False)
def add(request, id):
    if request.method == 'POST':
        form = SolutionAddForm(request.POST, request.FILES)
        if form.is_valid():
            solution = Solution(problem=Problem.objects.get(id=id))
            dir = str(solution.problem.path)
            solution.path = add_save_file(request.FILES['solution_file'], dir)
            solution.input = add_save_file(request.FILES['input_file'], dir)
            solution.output = add_save_file(request.FILES['output_file'], dir)
            solution.save()
            for choice in filter(lambda t: t[0] in form.cleaned_data['expected_verdicts'], form.fields['expected_verdicts'].choices):
                solution.expected_verdicts.add(choice.id)
            for choice in filter(lambda t: t[0] in form.cleaned_data['possible_verdicts'], form.fields['possible_verdicts'].choices):
                solution.possible_verdicts.add(choice.id)
            print(solution.possible_verdicts.__dict__)
            solution.save()
            return redirect(reverse('problem.views.problems.search_by_tag'))
            #TODO: change to reverse() here
    else:
        form = SolutionAddForm()
    return render_to_response('add_solution.html', {'form': form, 'id' : id},
        context_instance=RequestContext(request))

