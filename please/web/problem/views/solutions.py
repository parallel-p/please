from django.shortcuts import render_to_response
from django.template import RequestContext
from problem.models import Problem
from problem.forms import SolutionAddForm
from problem.helpers import problem_sync


@problem_sync(read=True, write=False)
def add(request, id):
    if request.method == 'POST':
        form = SolutionAddForm(request.POST)
        form.problem = Problem.objects.get(id=id)
        if form.is_valid():
            form.save()
            return redirect('/problems/{}/'.format(id))
    else:
        form = SolutionAddForm()
    return render_to_response('add_solution.html', {'form': form},
        context_instance=RequestContext(request))
