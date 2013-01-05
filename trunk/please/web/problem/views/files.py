from django.shortcuts import render_to_response
from django.template import RequestContext

from please.checkers import standard_checkers_utils

from problem.models import Problem
from problem.forms import ProblemUploadFilesForm, AdditonalUpload
from problem.views.file_utils import ChangeDir, file_save

from . import file_utils


def upload_main_block(request, problem):
    if request.method == 'POST' and 'upload_main' in request.POST:
        form = ProblemUploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['select_checker']:
                with ChangeDir(problem.path):
                    path = standard_checkers_utils.add_standard_checker_to_solution(form.cleaned_data['select_checker'])
                    problem.checker_path = path
            elif 'checker' in request.FILES.keys():
                problem.checker_path = str(request.FILES['checker'].name)
                file_save(problem, request.FILES['checker'])
            if 'validator' in request.FILES.keys():
                problem.validator_path = str(request.FILES['validator'].name)
                file_save(problem, request.FILES['validator'])
            problem.save()
    form = ProblemUploadFilesForm()
    return {'form': form, 'problem': problem}


def process_additional_upload(request, id):
    problem = Problem.objects.get(id=id)
    if request.method == 'POST':
        form = AdditonalUpload(request.POST, request.FILES)
        if form.is_valid():
            file_save(problem, request.FILES['uploaded'])
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
