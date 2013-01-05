import os.path

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from please.checkers import standard_checkers_utils

from problem.models import Problem
from problem.forms import ProblemUploadFilesForm, AdditonalUpload
from problem.helpers import problem_sync
from problem.views.file_utils import ChangeDir


from . import file_utils


def copy_to_problem(problem, path, data):
    with open(os.path.join(str(problem.path), str(path)), 'wb') as file:
        file.write(data.read())


def upload_main_dict(request, id):
    problem = Problem.objects.get(id=id)
    if request.method == 'POST':
        form = ProblemUploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['select_checker']:
                with ChangeDir(problem.path):
                    path = standard_checkers_utils.add_standard_checker_to_solution(form.cleaned_data['select_checker'])
                    problem.checker_path = path
            elif 'checker' in request.FILES.keys():
                problem.checker_path = str(request.FILES['checker'].name)
                copy_to_problem(problem, problem.checker_path, request.FILES['checker'])
            if 'validator' in request.FILES.keys():
                problem.validator_path = str(request.FILES['validator'].name)
                copy_to_problem(problem, problem.validator_path, request.FILES['validator'])
            problem.save()
    form = ProblemUploadFilesForm()
    return {'form': form, 'problem': problem, 'id': id}


def upload_main(request, id):
    return render_to_response('add_problem_files.html', {
            'upload_main_dict': upload_main_dict(request, id)
        }, RequestContext(request))


def process_additional_upload(request, id):
    problem = Problem.objects.get(id=id)
    if request.method == 'POST':
        form = AdditonalUpload(request.POST, request.FILES)
        if form.is_valid():
            copy_to_problem(problem, request.FILES['uploaded'].name, request.FILES['uploaded'])
            problem.save()
            form = AdditonalUpload()
    else:
        form = AdditonalUpload()

    return {'files': sorted(list(file_utils.list_files_flat(problem.path))),
            'form': form,
            'id': id}


def upload_additional_view(request, id):
    return render_to_response('upload_additional.html',
                              {'additional_upload': process_additional_upload(request, id)},
                              context_instance=RequestContext(request))
