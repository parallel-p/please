# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from problem.forms import ProblemEditMaterialsForm
from problem.models import Problem
import os

def problem_edit_confirm(request):
	return render_to_response('problem_edit_success.html')

def edit_problem_materials(request, id):
	model = Problem.objects.get(id=id)
	statement_abspath = os.path.join(str(model.path), str(model.statement_path))
	description_abspath = os.path.join(str(model.path), str(model.description_path))
	analysis_abspath = os.path.join(str(model.path), str(model.analysis_path))
	
	def load_files():
		exc_str = "Could not create {} file (wrong file path field?)"
		if not os.path.exists(statement_abspath):
			try:
				open(statement_abspath, 'w')
			except:
				raise Exception(exc_str.format('statement'))
		if not os.path.exists(description_abspath):
			try:
				open(description_abspath, 'w')
			except:
				raise Exception(exc_str.format('description'))
		if not os.path.exists(analysis_abspath):
			try:
				open(analysis_abspath, 'w')
			except:
				raise Exception(exc_str.format('analysis'))
		return (
			open(statement_abspath, 'r').read(),
			open(analysis_abspath, 'r').read(), 
			open(description_abspath, 'r').read()
		)

	if request.method == 'POST':
		form = ProblemEditMaterialsForm(request.POST)
		if form.is_valid():
			open(statement_abspath, 'w').write(form.cleaned_data["statement"])
			open(description_abspath, 'w').write(form.cleaned_data["description"])
			open(analysis_abspath, 'w').write(form.cleaned_data["analysis"])
			# Here we have to do "git commit".
			return redirect('/problem/confirmation/')
	else:
		vals = load_files()
		form = ProblemEditMaterialsForm(initial={
			'statement': vals[0],
			'description': vals[2],
			'analysis': vals[1]
		})
	return render_to_response('edit_problem_materials.html', {
			'form': form
		}, RequestContext(request))

def list_problems(request, problem_list=None):
    if problem_list is None:
        problem_list = Problem.objects.all()
    return render_to_response('list_problems.html', {'problems' : problem_list},
        context_instance=RequestContext(request))
