# Create your views here.
from django.shortcuts import render_to_response
from django.http import redirect
from problem.forms import ProblemEditMaterialsForm
from problem.models import Problem

def edit_problem_materials(request, id=None):
	if request.method == 'POST':
		form = ProblemEditForm(request.POST, instance=Problem.objects.get(id=id))
		if form.is_valid():

			return redirect('/thanks/')
	else:
		form = ProblemEditMaterialsForm(instance=Problem.objects.get(id=id))
		form.load_files()
	return render_to_response(request, 'edit_problem_materials.html', {
			'form': Form,
		})