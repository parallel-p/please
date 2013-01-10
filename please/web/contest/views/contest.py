from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

from ..models import Contest
from .contests import edit_or_create_contest_block

def index(request, id):
    contest = get_object_or_404(Contest, id=id)
    return render_to_response('contest/index.html', {
        'contest': contest,
        'edit_contest': edit_or_create_contest_block(request, contest),
    }, RequestContext(request))

