import re
import os.path
from django import forms
from contest.models import *
from please import export_servers

class AddContestForm(forms.Form):
    path = forms.CharField(required=True)

def choices():
    contests = Contest.objects.all()
    return [[contest.id, str(contest)] for contest in contests]

class CopyContestForm(forms.Form):
    contest = forms.ChoiceField(choices=choices())
    new_contest_file = forms.CharField(required=True)

def servers():
    servers = export_servers.servers.keys()
    return [[server, server] for server in servers]

class ExportToTesterForm(forms.Form):
    server = forms.ChoiceField(required=True, choices=servers())
    server_contest_id = forms.CharField(required=True)

class AddContestProblemForm(forms.ModelForm):
    class Meta:
        model = ContestProblem
        fields = ('id_in_contest', 'problem')

class ContestEditForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ('path', 'name', 'id_method', 'statement_name', 'statement_location', 'statement_date', 'statement_template')

class EmptyForm(forms.Form):
    pass
