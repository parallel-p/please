from django.db import models

class Tag(models.Model):
	name = models.CharField(max_length=64)

	def __str__(self):
		return str(self.name)

class Verdict(models.Model):
	name = models.CharField(max_length=2)

	def __str__(self):
		return str(self.name)

class Solution(models.Model):
	expected_verdicts = models.ManyToManyField(Verdict)
	possible_verdicts = models.ManyToManyField(Verdict)
	problem = models.ForeignKey('Problem')
	fname = models.CharField(max_length=256)
	path_or_stdin = models.CharField(max_length=64)
	path_or_stdout = models.CharField(max_length=64)

	def __str__(self):
		return str(self.problem) + ': solution ' + str(self.fname)