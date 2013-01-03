from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from problem.models import Problem
from problem.forms import ProblemEditForm, ProblemSearch
from problem.synchronization import export_from_database, import_to_database
from please.template.problem_template_generator import generate_problem
import os


def create(request):
    model = Problem()
    model.save()
    
    import_to_database(model, "../templates/Template/")
    if request.method == 'POST':
        form = ProblemEditForm(request.POST)
        if form.is_valid():
            cur_path = os.getcwd()
            os.chdir(form.cleaned_data["path"])
            generate_problem(form.cleaned_data["short_name"])
            os.chdir(cur_path)
                        
            model.checker_path = 'checker.cpp'
            model.path = os.path.join(form.cleaned_data["path"], form.cleaned_data["short_name"])
            model.name = form.cleaned_data["short_name"]
            model.short_name = form.cleaned_data["short_name"]
            model.input = form.cleaned_data["input"]
            model.output = form.cleaned_data["output"]
            model.time_limit = float(form.cleaned_data["time_limit"])
            model.memory_limit = int(form.cleaned_data["memory_limit"])
            model.save()
            export_from_database(model)
            
            return redirect('/problems/confirmation/')
    else:
        form = ProblemEditForm()
    return render_to_response('create_problem.html', {
            'form': form
        }, RequestContext(request))


def add(request):
    if request.method == 'POST':
        form = AddProblemForm(request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']
            problem = Problem(path=path)
            problem.save()
            import_to_database(problem)
            problem.save()
            return redirect('/problems/confirmation')
    else:
        form = AddProblemForm()
    return render_to_response('problem_add.html', {'form': form}, RequestContext(request))


def problems_list(problems):
    return render_to_response("problems_list.html", {"problems": problems})


def search_by_tag(request):
    form = ProblemSearch(request.GET)
    form.is_valid()
    if form.cleaned_data["tags"] == "":
        return render_to_response("problems_search_by_tag.html", {
            "form": form,
            "problems": Problem.objects.all()
        })
    else:
        return problems_list(Problem.objects.filter(tags__name__contains=form.cleaned_data["tags"]).distinct())
