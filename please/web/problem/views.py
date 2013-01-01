# Create your views here.
from django.shortcuts import render_to_response
from django.http import redirect
from problem.views import ProblemEditForm
from problem.models import Problem

def edit_problem_materials(request, id=None):
	if id is None:
		if request.method == 'POST':
			pass
		else:
			form = ProblemEditForm()
	else:
		if request.mathod == 'POST':
			pass
		else:
			form = ProblemEditForm(instance=Problem.objects.get(id=id))
			form.load_files()
	return render_to_response(request, 'edit_problem_materials.html', {
			'form': Form,
		})