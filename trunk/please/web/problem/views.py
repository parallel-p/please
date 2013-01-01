# Create your views here.
from django.shortcuts import render_to_response
#from django.http import redirect
#from problem.forms import ProblemEditMaterialsForm
from problem.models import Problem
from django.template import RequestContext

#def edit_problem_materials(request, id=None):
#	if request.method == 'POST':
#		form = ProblemEditForm(request.POST, instance=Problem.objects.get(id=id))
#		if form.is_valid():
#
#			return redirect('/thanks/')
#	else:
#		form = ProblemEditMaterialsForm(instance=Problem.objects.get(id=id))
#		form.load_files()
#	return render_to_response(request, 'edit_problem_materials.html', {
#			'form': Form,
#		})# Create your views here.

def list_problems(request, problem_list=None):
    if problem_list is None:
        problem_list = Problem.objects.all()
    return render_to_response('list_problems.html', {'problems' : problem_list},
        context_instance=RequestContext(request))
