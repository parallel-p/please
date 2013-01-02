from django import forms
from problem.models import *


class ProblemEditForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('path', 'name', 'input', 'output', 'time_limit', 'memory_limit')


class ProblemSearch(forms.Form):
    tags = forms.CharField(required=False)


class ProblemEditMaterialsForm(forms.Form):
    statement = forms.CharField(widget=forms.Textarea, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    analysis = forms.CharField(widget=forms.Textarea, required=False)


class ProblemUploadFilesForm(forms.Form):
    checker = forms.FileField(required=False)
    validator = forms.FileField(required=False)


class SolutionAddForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ('problem',)
