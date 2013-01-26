import re
import os.path
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
    available_tags = forms.MultipleChoiceField(
                required=False, 
                choices=((tag, tag.name) for tag in ProblemTag.objects.all())
            ) if ProblemTag.objects.count() > 0 else ""
    new_tags = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': 'add your own tag(s)'}),
            required=False,
            label=''
        )


class ProblemSearch(forms.Form):
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'search by tag',
        'class': 'search-query',
    }))


class ProblemEditMaterialsForm(forms.Form):
    statement = forms.CharField(widget=forms.Textarea, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    analysis = forms.CharField(widget=forms.Textarea, required=False)


standart_checkers = [('', 'select default'),
                     ('acmp', 'acmp'),
                     ('dcmp', 'dcmp'),
                     ('fcmp', 'fcmp'),
                     ('hcmp', 'hcmp'),
                     ('icmp', 'icmp'),
                     ('lcmp', 'lcmp'),
                     ('ncmp', 'ncmp'),
                     ('rcmp', 'rcmp'),
                     ('rcmp4', 'rcmp4'),
                     ('rcmp6', 'rcmp6'),
                     ('rcmp9', 'rcmp9'),
                     ('rncmp', 'rncmp'),
                     ('wcmp', 'wcmp'),
                     ('yesno', 'yesno')]


class ProblemUploadFilesForm(forms.Form):
    checker = forms.FileField(required=False)
    select_checker = forms.ChoiceField(required=False, choices=standart_checkers)
    validator = forms.FileField(required=False)


class SolutionAddForm(forms.Form):
    solution_file = forms.FileField(required=True)
    input_file_name = forms.CharField(required=False)
    output_file_name = forms.CharField(required=False)
    expected_verdicts = forms.MultipleChoiceField(
            widget=forms.SelectMultiple(attrs={'size': 6}),
            choices=[(verdict, verdict.name) for verdict in Verdict.objects.all()],
            required=True,
            initial=["OK"])
    possible_verdicts = forms.MultipleChoiceField(
            widget=forms.SelectMultiple(attrs={'size': 6}),
            choices=[(verdict, verdict.name) for verdict in Verdict.objects.all()],
            required=False)


class ProblemImportFromPolygonForm(forms.Form):
    target_path = forms.CharField(required=True, max_length=255)
    contest_id = forms.IntegerField(required=True)
    problem_letter = forms.CharField(required=True, max_length=1)


class ManageTestsForm(forms.Form):
    tests_please_content = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )


class AdditonalUpload(forms.Form):
    uploaded = forms.FileField(required=True, label='Select file')


def upload_files_form(path_str):
    class UploadFiles(forms.Form):
        path = forms.FilePathField(
            path=path_str,
            allow_files=False, allow_folders=True,
            required=False, recursive=True
        )

        path.choices[0] = (path_str, os.path.sep)
        choices = []
        for choice in path.choices:
            if not re.match(r'^[/\\]\.', choice[1]):
                choices.append(choice)
        path.choices = choices

        file = forms.FileField(required=False, widget=forms.FileInput(attrs={
            'multiple': 'multiple',
        }))
    return UploadFiles


def tags_edit_form(problem):
    class EditTagsForm(forms.Form):
        added_tags = forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(attrs={'checked': 'checked'}),
            choices=((tag, tag.name) for tag in problem.tags.all()),
            required=False
        ) if problem.tags.count() > 0 else "no tags matching the problem"
        other_tags = forms.MultipleChoiceField(
            choices=[(tag, tag.name) for tag in ProblemTag.objects.all() if tag not in problem.tags.all()],
            required=False
        ) if ProblemTag.objects.count() > problem.tags.count() else ''
        add_tag = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'placeholder': 'or add your own' if ProblemTag.objects.count() > problem.tags.count() else 'add your own tag'
        }))
    return EditTagsForm


class EmptyForm(forms.Form):
    pass

def choices():
    problems = Problem.objects.all()
    return [[problem.id, str(problem)] for problem in problems]

class CopyProblemForm(forms.Form):
    problem = forms.ChoiceField(choices=choices())
    copy_to = forms.CharField(required=True)
