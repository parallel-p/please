from django import forms

class ProblemEditMaterialsForm(forms.Form):
	statement = forms.CharField(widget=forms.Textarea, required=False)
	description = forms.CharField(widget=forms.Textarea, required=False)
	analysis = forms.CharField(widget=forms.Textarea, required=False)
