from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

#from please.template.problem_template_generator import generate_problem
#from please.import_from_polygon import download_zip, create_problem
#from please.cleaner.cleaner import Cleaner
#from please import globalconfig

from please.contest.commands import command_create_contest
from contest.models import Contest                   
from contest.forms import AddContestForm, ContestEditForm
from contest.synchronization import import_to_database, export_from_database, is_contest_path
from please.web.problem.views.file_utils import ChangeDir, file_read

import os

class NoDirectoryException(Exception):
    pass


class ContestExistsException(Exception):
    pass




def import_from_polygon(request):
    return render_to_response('contests/import_from_polygon.html', {})

def add_tree(request):
    return render_to_response('contests/add_tree.html', {})

def add(request):
    block = add_contest_block(request)
    if block['is_success']:
        return redirect(reverse('contest.views.contests.index'))
    return render_to_response('contests/add.html', {
        'nav': 'add',
        'add_contest': block,
    }, RequestContext(request))

def add_contest_block(request):
    is_success, is_error = False, False
    if request.method == 'POST':
        form = AddContestForm(request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']
            if is_contest_path(path):
                contest = Contest(path=path)
                contest.save()
                import_to_database(contest)
                contest.save()
                is_success = True
            else:
                is_error = True
    else:
        form = AddContestForm()
    return {
        'form': form,
        'is_success': is_success,
        'is_error': is_error,
    }


def create(request):
    block = edit_or_create_contest_block(request)
    if block['is_success']:
        return redirect(reverse('contest.views.contests.index'))
    return render_to_response('contests/create.html', {
        'nav': 'create',
        'edit_contest': block,
    }, RequestContext(request))

def edit_or_create_contest_block(request, contest=None):
    is_success = False
    if request.method == 'POST':
        form = ContestEditForm(request.POST)
        if form.is_valid():
            if contest is None:
                if not os.path.exists(form.cleaned_data["path"]):
                    raise NoDirectoryException("There is no such directory!")
                if os.path.exists(os.path.join(form.cleaned_data["path"], form.cleaned_data["name"])):
                    raise ContestExistsException("This contest already exists")
                contest = Contest()
                contest.path = os.path.join(form.cleaned_data["path"], form.cleaned_data["name"])
                with ChangeDir(form.cleaned_data["path"]):
                    command_create_contest(form.cleaned_data["name"], [])
            contest.name = form.cleaned_data["name"]
            contest.id_method = form.cleaned_data["id_method"]
            contest.statement_name = form.cleaned_data["statement_name"]
            contest.statement_location = form.cleaned_data["statement_location"]
            contest.statement_date = form.cleaned_data["statement_date"]
            contest.statement_template = form.cleaned_data["statement_template"]
            contest.save()
            export_from_database(contest)
            is_success = True
    else:
        if contest is None:
            form = ContestEditForm()
        else:
            form = ContestEditForm(initial={
                'name': contest.name,
                'id_method': contest.id_method,
                'statement_name': contest.statement_name,
                'statement_location': contest.statement_location,
                'statement_date': contest.statement_date,
                'statement_template': contest.statement_template,
            })
    return {
        'form': form,
        'is_success': is_success,
    }

def index(request):
    return render_to_response('contests/index.html', {
        'navbar': 'contests',
        'contests_list': Contest.objects.all(),
    }, RequestContext(request))


def add_contest_block(request):
    is_success, is_error = False, False
    if request.method == 'POST':
        form = AddContestForm(request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']
            if is_contest_path(path):
                contest = Contest(path=path)
                contest.save()
                import_to_database(contest)
                contest.save()
                is_success = True
            else:
                is_error = True
    else:
        form = AddContestForm()
    return {
        'form': form,
        'is_success': is_success,
        'is_error': is_error,
    }
