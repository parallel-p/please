import os
from please import globalconfig

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

from ..models import Contest, ContestProblem
from ..forms import AddContestProblemForm, ExportToTesterForm
from .contests import edit_or_create_contest_block
from please.contest.commands import command_generate_statement, command_export
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
    ContestProblem.objects.get(id=problem_id).delete()
    probs = ContestProblem.objects.filter(contest__id=id)
    for i in range(len(probs)):
        probs[i].order = i
        probs[i].save()
    return redirect('/contests/{}'.format(id))

def insert_problem(request, contest):
    if request.method == 'POST':
        form = AddContestProblemForm(request.POST)
        if form.is_valid():
            problem = form.cleaned_data['problem']
            id_in_contest = form.cleaned_data['id_in_contest']
            order = ContestProblem.objects.filter(contest=contest).count()
            ContestProblem(problem=problem, id_in_contest=id_in_contest, order=100, contest=contest).save()           
    else:
        form = AddContestProblemForm()
    return {
        'form': form,
    }

@contest_sync(read=True, write=True)
def problem_up(request, id, problem_id):
    prob2 = ContestProblem.objects.get(id=problem_id)
    prob1 = ContestProblem.objects.get(order=prob2.order - 1, contest__id=id)
    print(prob1.order, prob2.order)
    prob1.order, prob2.order = prob2.order, prob1.order
    print(prob1.order, prob2.order)
    prob1.save()
    prob2.save()
    return redirect('/contests/{}'.format(id))

@contest_sync(read=True, write=True)
def problem_down(request, id, problem_id):
    prob2 = ContestProblem.objects.get(id=problem_id)
    prob1 = ContestProblem.objects.get(order=prob2.order + 1, contest__id=id)
    prob1.order, prob2.order = prob2.order, prob1.order
    prob1.save()
    prob2.save()
    return redirect('/contests/{}'.format(id))

def export_to_tester(request, id):
    block = export_to_tester_block(request, id)
    if block['is_success']:
        return redirect(reverse('contest.views.contests.index'))
    return render_to_response('contest/export_to_tester.html', {
        'export_to_tester': block,
        'id': id,
    }, RequestContext(request))

def export_to_tester_block(request, id):
    is_success = False
    if request.method == 'POST':
        contest = get_object_or_404(Contest, id=id)
        form = ExportToTesterForm(request.POST)
        if form.is_valid():
            server_contest_id = form.cleaned_data['server_contest_id']
            server = form.cleaned_data['server']
            print(contest.path, contest)
            with ChangeDir(os.path.dirname(contest.path)):
                command_export(os.path.basename(contest.path)[:-8], server, server_contest_id)
            is_success = True
    else:
        form = ExportToTesterForm()
    return {
        'is_success': is_success,
        'form': form,
    }

