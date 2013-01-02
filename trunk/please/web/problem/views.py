from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from problem.forms import (
    ProblemEditMaterialsForm,
    ProblemSearch,
    ProblemUploadFilesForm,
    ProblemEditForm,
    SolutionAddForm,
    TestsForm
)
import problem
from problem.models import Problem
from please.template.problem_template_generator import *
from problem.synchronization import *
import os
import os.path
from os import chdir

def create_problem(request):
    if request.method == 'POST':
        form = ProblemEditForm(request.POST)
        if form.is_valid():
            cur_path = os.getcwd()
            chdir(form.cleaned_data["path"])
            generate_problem(form.cleaned_data["name"])
            chdir(cur_path)
            model = form.save()
            model.path += model.name
            export_from_database(model)
            return redirect('/problem/confirmation/')
    else:
        form = ProblemEditForm()
    return render_to_response('create_problem.html', {
            'form': form
        }, RequestContext(request))


def add_problem_files(request, id):
    model = Problem.objects.get(id=id)
    if request.method == 'POST':
        form = ProblemUploadFilesForm(request.POST, request.FILES)
        if form.is_valid() and len(request.FILES) > 0:
            if 'checker' in request.FILES.keys():
                checker_fpath, checker_fname = os.path.split(str(model.checker_path))
                checker_fname = request.FILES['checker'].name
                model.checker_path = os.path.join(checker_fpath, checker_fname)
                open(os.path.join(
                        str(model.path),
                        str(model.checker_path)
                    ), 'wb').write(request.FILES['checker'].read())
            if 'validator' in request.FILES.keys():
                validator_fpath, validator_fname = os.path.split(str(model.validator_path))
                validator_fname = request.FILES['validator'].name
                model.validator_path = os.path.join(validator_fpath, validator_fname)
                open(os.path.join(
                        str(model.path),
                        str(model.validator_path)
                    ), 'wb').write(request.FILES['validator'].read())
            model.save()
            return redirect('/problem/confirmation/')
    else:
        form = ProblemUploadFilesForm()
    return render_to_response('add_problem_files.html', {
            'form': form,
            'model': model,
            'id': id
        }, RequestContext(request))


def problems_list(problems):
    return render_to_response("problems_list.html", {"problems": problems})


def problems_search_by_tag(request):
    form = ProblemSearch(request.GET)
    form.is_valid()
    if form.cleaned_data["tags"] == "":
        return render_to_response("problems_search_by_tag.html", {
            "form": form,
            "problems": Problem.objects.all()
        })
    else:
        return problems_list(Problem.objects.filter(tags__name__contains=form.cleaned_data["tags"]).distinct())


def add_solution(request, id):
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


def tests(request, id):
    problem = get_object_or_404(Problem.objects, id=id)
    if request.method == 'POST':
        form = TestsForm(request.POST)
        if form.is_valid():
            with open(os.path.join(problem.path, "tests.please"), "w") as tp_file:
                tp_file.write(form.cleaned_data["tests_please_content"])
    else:
        with open(os.path.join(problem.path, "tests.please"), "r") as tp_file:
            content = tp_file.read()
        form = TestsForm(initial={"tests_please_content": content})

    return render_to_response("tests.html", {
        "form": form,
    }, RequestContext(request))


def upload_additional():
    form = problem.forms.AdditonalUpload()
