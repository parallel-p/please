import re
import os.path
from django import forms
from contest.models import *


class AddContestForm(forms.Form):
    path = forms.CharField(required=True)

class AddContestProblemForm(forms.Form):
    class Meta:
        model = ContestProblem
        fields = ('problem', 'id_in_contest')

class ContestEditForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ('path', 'name', 'id_method', 'statement_name', 'statement_location', 'statement_date', 'statement_template')

class EmptyForm(forms.Form):
    pass
