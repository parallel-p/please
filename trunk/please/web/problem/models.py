from django.db import models

class Problem(models.Model):
	pass

class Tag(models.Model):
	name = models.CharField(max_length=64)

	def __str__(self):
		return str(self.name)

class Solution(models.Model):
	tag = models.ManyToManyField(Tag)
	problem = models.ForeignKey(Problem)
	fname = models.CharField(max_length=256)
	path_or_stdin = models.BooleanField()
	path_or_stdout = models.BooleanField()

class Verdict(models.Model):
	solution = models.ForeignKey(Solution)
	name = models.CharField(max_length=2)
	expected = models.BooleanField()

	def __str__(self):
		return str(self.solution) + ': ' + str(self.name) + (' (possible)' if not bool(self.expected) else ' (expected)')
