from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from problem.forms import ProblemEditMaterialsForm
from problem.models import Problem
from problem.helpers import problem_sync
import os


def edit_load_files(*args):
    print(args)
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
                open(statement_abspath, 'w', encoding='utf-8').write(form.cleaned_data["statement"])
            if not vals[1][1]:
                open(description_abspath, 'w', encoding='utf-8').write(form.cleaned_data["description"])
            if not vals[2][1]:
                open(analysis_abspath, 'w', encoding='utf-8').write(form.cleaned_data["analysis"])
            # Here we have to do "git commit".
            return redirect('/problems/confirmation/')
    else:
        print(vals)
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
