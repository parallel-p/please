import re
import os.path
from django import forms
from contest.models import *


class AddContestForm(forms.Form):
    path = forms.CharField(required=True)

def choices():
    contests = Contest.objects.all()
    return [[contest.id, str(contest)] for contest in contests]

class CopyContestForm(forms.Form):
    contest = forms.ChoiceField(choices=choices())
    new_contest_file = forms.CharField(required=True)

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
