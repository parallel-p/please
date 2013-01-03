from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from problem.models import Problem
from problem.forms import ProblemUploadFilesForm, AdditonalUpload
from problem.helpers import problem_sync
import os.path


def copy_to_problem(problem, path, data):
    with open(os.path.join(str(problem.path), str(path)), 'wb') as file:
        file.write(data.read())


@problem_sync(read=True, write=False)
def upload_main(request, id):
    problem = Problem.objects.get(id=id)
    if request.method == 'POST':
        form = ProblemUploadFilesForm(request.POST, request.FILES)
        if form.is_valid() and len(request.FILES) > 0:
            if 'checker' in request.FILES.keys():
                copy_to_problem(problem, os.path.join(problem.checker_path, str(request.FILES['checker'].name)), request.FILES['checker'])
            if 'validator' in request.FILES.keys():
                copy_to_problem(problem, os.path.join(problem.validator_path, str(request.FILES['validator'].name)), request.FILES['validator'])
            problem.save()
            return redirect('/problems/confirmation/')
    else:
        form = ProblemUploadFilesForm()
    return render_to_response('add_problem_files.html', {'form': form,
                                                         'problem': problem,
                                                         'id': id},
                              RequestContext(request))


def upload_additional(request, id):
    problem = Problem.objects.get(id=id)
    if request.method == 'POST':
        form = AdditonalUpload(request.POST, request.FILES)
        if form.is_valid():
            copy_to_problem(problem, request.FILES['uploaded'].name, request.FILES['uploaded'])
            problem.save()
            return redirect(request.path)
    else:
        form = AdditonalUpload()

    uploaded_files = [i for i in os.listdir(problem.path) if i[0] != '.']

    return render_to_response('upload_additional.html',
                              {'uploaded_files': uploaded_files,
                               'additional_upload_form': form,
                               'problem_id': problem.id},
                              context_instance=RequestContext(request))
