from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from problem.forms import ProblemEditMaterialsForm
from problem.models import Problem
from problem.helpers import problem_sync
from problem.views.file_utils import file_write
from please.latex.latex_tools import generate_problem
from please import globalconfig
import os


def edit_load_files(*args):
    exc_str = "Could not create {} file (wrong file path field?)"
    fnames = ('statement', 'description', 'analysis')
    result = [['', False] for i in args]
    for num, path in enumerate(args):
        if os.path.isfile(path):
            result[num][0] = open(path, 'r', encoding='utf-8').read()
        else:
            try:
                open(path, 'w', encoding='utf-8')
            except:
                result[num] = [exc_str.format(fnames[num]), True]
    return result


@problem_sync(read=True, write=False)
def edit(request, id):
    model = Problem.objects.get(id=id)
    statement_abspath = os.path.join(str(model.path), str(model.statement_path))
    description_abspath = os.path.join(str(model.path), str(model.description_path))
    analysis_abspath = os.path.join(str(model.path), str(model.analysis_path))
    vals = edit_load_files(statement_abspath, description_abspath, analysis_abspath)
    if request.method == 'POST':
        form = ProblemEditMaterialsForm(request.POST)
        if form.is_valid():
            if not vals[0][1]:
                file_write(form.cleaned_data["statement"], statement_abspath)
            if not vals[1][1]:
                file_write(form.cleaned_data["description"], description_abspath)
            if not vals[2][1]:
                file_write(form.cleaned_data["analysis"], analysis_abspath)
            # Here we have to do "git commit".
            return redirect('/problems/confirmation/')
    else:
        form = ProblemEditMaterialsForm(initial={
            'statement': vals[0][0],
            'description': vals[1][0],
            'analysis': vals[2][0],
        })
        for num, name in enumerate(('statement', 'description', 'analysis')):
            if vals[num][1]:
                form.fields[name].widget.attrs['readonly'] = True
    return render_to_response('edit_problem_materials.html', {
            'form': form,
            'problem_id': id,
        }, RequestContext(request))

def gen_statement(request, id):
    problem = get_object_or_404(Problem.objects, id=id)
    file_exists = os.path.isfile(
        os.path.join(problem.path, problem.statement_path)
    )
    if request.method == 'POST':
        cwd = os.getcwd()
        os.chdir(str(problem.path))
        pdf_path = os.path.abspath(os.path.join(
            globalconfig.statements_dir,
            os.path.basename(generate_problem())
        ))
        os.chdir(cwd)
        response = HttpResponse(FileWrapper(open(pdf_path, 'rb')), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(pdf_path))
        return response
    return render_to_response('generate_statement.html', {
            'id': id,
            'file_exists': file_exists
        }, RequestContext(request))
