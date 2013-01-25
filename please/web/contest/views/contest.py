import os
from please import globalconfig

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

from ..models import Contest, ContestProblem
from ..forms import AddContestProblemForm
from .contests import edit_or_create_contest_block
from please.contest.commands import command_generate_statement
from please.web.problem.views.file_utils import ChangeDir
from ..helpers import contest_sync

@contest_sync(read=True, write=True)
def index(request, id):
    contest = get_object_or_404(Contest, id=id)
    if request.method == 'POST' and 'save_and_generate' in request.POST:
        with ChangeDir(os.path.dirname(contest.path)):
            command_generate_statement(os.path.basename(contest.path[:-8]))
    return render_to_response('contest/index.html', {
        'contest': contest,
        'insert_problem': insert_problem(request, contest),
        'edit_contest': edit_or_create_contest_block(request, contest),
        'pdf_exists': os.path.isfile(os.path.abspath(os.path.join(
                os.path.dirname(contest.path), 
                os.path.splitext(os.path.basename(contest.path))[0] + '.pdf')))
    }, RequestContext(request))

def view_statement(request, id):
    contest = get_object_or_404(Contest.objects, id=id)
    pdf_path = os.path.abspath(
            os.path.join(
                os.path.dirname(contest.path),
                os.path.splitext(
                    os.path.basename(contest.path))[0] + '.pdf'))
    return HttpResponse(FileWrapper(open(pdf_path, 'rb')), content_type='application/pdf')
    
@contest_sync(read=False, write=True)
def delete_problem(request, id, problem_id):
    ContestProblem.objects.filter(problem__id=problem_id, contest__id=id).delete()
    return redirect('/contests/{}'.format(id))

def insert_problem(request, contest):
    if request.method == 'POST':
        form = AddContestProblemForm(request.POST)
        if form.is_valid():
            problem = form.cleaned_data['problem']
            id_in_contest = form.cleaned_data['id_in_contest']
            ContestProblem(problem=problem, id_in_contest=id_in_contest, order=100, contest=contest).save()           
    else:
        form = AddContestProblemForm()
    return {
        'form': form,
    }
