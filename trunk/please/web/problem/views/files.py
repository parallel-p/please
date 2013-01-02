from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from problem.models import Problem
from problem.forms import ProblemUploadFilesForm, AdditonalUpload
import os.path


def upload_main(request, id):
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
            return redirect('/problems/confirmation/')
    else:
        form = ProblemUploadFilesForm()
    return render_to_response('add_problem_files.html', {
            'form': form,
            'model': model,
            'id': id
        }, RequestContext(request))

def upload_additional():
    form = problem.forms.AdditonalUpload()
