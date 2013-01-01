from django import forms
from problem.models import Problem

class ProblemEditMaterialsForm(forms.Form):
	statement = forms.TextField()
	analysis = forms.TextField()
	description = forms.TextField()

	class Meta:
		model = Problem

	def load_files(self):
		self.statement = open(str(self.instance.statement_path), 'r').read()
		self.analysis = open(str(self.instance.analysis_path), 'r').read()
		seld.description = open(str(self.instance.description_path, 'r').read()

	def edit_fields(self):
		return r'''<p>Statement:<br /><textarea>{}</textarea></p>
		           <p>Description:<br /><textarea>{}</textarea></p>
		           <p>Analysis:<br /><textarea>{}</textarea></p>'''.format(
		           		str(self.statement),
		           		str(self.description),
		           		str(self.analysis)
		            )