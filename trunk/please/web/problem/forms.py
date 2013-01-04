from django import forms
from problem.models import *


class AddProblemForm(forms.Form):
    path = forms.CharField(max_length=255, required=True)


class AddTestsForm(forms.Form):
    test = forms.FileField(label='Specify a test file (or a zip archive with test files)')


class ProblemEditForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('path', 'name', 'short_name', 'input', 'output', 'time_limit', 'memory_limit')


class ProblemSearch(forms.Form):
    tags = forms.CharField(required=False)


class ProblemEditMaterialsForm(forms.Form):
    statement = forms.CharField(widget=forms.Textarea, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    analysis = forms.CharField(widget=forms.Textarea, required=False)


class ProblemUploadFilesForm(forms.Form):
    checker = forms.FileField(required=False)
    validator = forms.FileField(required=False)


class SolutionAddForm(forms.Form):
    solution_file = forms.FileField(required=True)
    input_file_name = forms.CharField(required=False)
    output_file_name = forms.CharField(required=False)
    expected_verdicts = forms.MultipleChoiceField(
            choices=[(verdict, verdict.name) for verdict in Verdict.objects.all()],
            required=True,
            initial=["OK"])
    possible_verdicts = forms.MultipleChoiceField(
            choices=[(verdict, verdict.name) for verdict in Verdict.objects.all()],
            required=False)


class TestsForm(forms.Form):
    tests_please_content = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        required=False
    )


class AdditonalUpload(forms.Form):
    uploaded = forms.FileField(required=True, label='Select file')
