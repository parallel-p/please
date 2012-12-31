from django.db import models


class RunErrorDescription(models.Model):
	stdout = models.TextField(blank=True)
	stderr = models.TextField(blank=True)
	exit_code = models.IntegerField()


class TestGeneratorError(models.Model):
	description = models.ForeignKey(RunErrorDescription, null=False)


class TestError(models.Model):
	PROGRAM_TYPES = (
		('v', 'validator'),
		('c', 'checker'),
	)
	program_type = models.CharField(max_length=1, choices=PROGRAM_TYPES)
	command_line = models.CharField(max_length=500)
	description = models.ForeignKey(RunErrorDescription, null=False)


class TestGeneratorTag(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class TestGenerator(models.Model):
	tags = models.ManyToManyField(TestGeneratorTag, related_name='+', blank=True)
	script = models.CharField(max_length=500)
	error = models.ForeignKey(TestGeneratorError, blank=True, null=True)

	def __str__(self):
		return self.script


class Test(models.Model):
	generator = models.ForeignKey(TestGenerator, null=False)
	error = models.ForeignKey(TestError, blank=True, null=True)


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

