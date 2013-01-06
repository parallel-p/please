from zipfile import ZipFile
from problem.forms import upload_files_form
from problem.views.file_utils import *


def upload_files(request, problem):
    UploadFilesForm = upload_files_form(problem.path)

    if request.method == 'POST' and 'upload_files' in request.POST:
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data["file"] is not None:
            path = form.cleaned_data["path"]
            for temp_file in request.FILES.getlist('file'):
                if temp_file.content_type == 'application/zip':
                    ZipFile(temp_file).extractall(path)
                else:
                    file_save(temp_file, path)
    else:
        form = UploadFilesForm()

    return {'form': form, 'problem_id': problem.id}
