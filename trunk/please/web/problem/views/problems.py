from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from problem.models import Problem
from problem.forms import ProblemEditForm, ProblemSearch, AddProblemForm
from problem.synchronization import export_from_database, import_to_database
from please.template.problem_template_generator import generate_problem
from django.core.exceptions import ObjectDoesNotExist
import os


class NoDirectoryException(Exception):
    pass


class ProblemExistsException(Exception):
    pass


def import_to_database_advanced(model, path):
    template_problem = None
    for problem in Problem.objects.all():
        if problem.name == "Template_problem_for_please":
            template_problem = problem
            break
    if template_problem is None:
        model.save()
        import_to_database(model, path)
    else:
        model = template_problem
    return model

def create(request, id = None):
    problem_id = id
    model = Problem()
    try:
        model = Problem.objects.get(id=id)
    except ObjectDoesNotExist:
        problem_id = None    
        
    if problem_id is None:
        model = import_to_database_advanced(model, "../templates/Template/")
            

    if request.method == 'POST':
        form = ProblemEditForm(request.POST)
        if form.is_valid():
            if problem_id is None:
                old_path = os.getcwd()
                if not os.path.exists(form.cleaned_data["path"]):
                    raise NoSuchDirectoryException("There is no such directory!")
                model.path = os.path.join(form.cleaned_data["path"], form.cleaned_data["short_name"])
                if os.path.exists(model.path):
                    raise ProblemExistsException("This problem already exists")
                os.chdir(form.cleaned_data["path"])
                generate_problem(form.cleaned_data["short_name"])
                os.chdir(old_path)
                
            model.name = form.cleaned_data["name"]
            model.short_name = form.cleaned_data["short_name"]
            model.input = form.cleaned_data["input"]
            model.output = form.cleaned_data["output"]
            model.time_limit = float(form.cleaned_data["time_limit"])
            model.memory_limit = int(form.cleaned_data["memory_limit"])
            model.save()
            export_from_database(model)

            return redirect('/problems/confirmation/')
    else:
        if problem_id is None:
            form = ProblemEditForm()
        else:
            form = ProblemEditForm(initial = {'name': model.name, 'short_name': model.short_name})

    return render_to_response('create_problem.html', {
            'form': form,
            'problem_id': problem_id,
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
