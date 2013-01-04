from zipfile import ZipFile
from django.shortcuts import get_object_or_404
from problem.models import Problem
from problem.forms import upload_files_form
from problem.views.file_utils import *

def upload_files(request, problem):
    UploadFilesForm = upload_files_form(problem.path)

    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data["file"] is not None:
            path = form.cleaned_data["path"]
            temp_file = form.cleaned_data["file"]

            if temp_file.content_type == 'application/zip':
                ZipFile(temp_file).extractall(path)
            else:
                file_save(temp_file, path)
    else:
        form = UploadFilesForm()

    return {'form': form, 'problem_id': problem.id}
