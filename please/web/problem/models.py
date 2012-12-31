from django.db import models

class Problem(models.Model):
    name = models.CharField(max_length = 100)
    short_name = models.CharField(max_length = 100)
    tags = models.ManyToManyField('Tag')

    input = models.CharField(max_length = 100)
    output = models.CharField(max_length = 100)
    time_limit = models.FloatField()
    memory_limit = models.IntegerField()

    checker = models.CharField(max_length = 100)
    validator = models.CharField(max_length = 100)
    main_solution = models.CharField(max_length = 100)

    statement = models.CharField(max_length = 100)
    description = models.CharField(max_length = 100)

    hand_answer_extension = models.CharField(max_length = 100)

    well_done_test = models.CharField(max_length = 100)
    well_done_answers = models.CharField(max_length = 100)

    analysis = models.CharField(max_length = 100)

    def __str__(self):
        return "Problem {}".format(self.name)


class RunErrorDescription(models.Model):
	stdout = models.TextField(blank=True)
	stderr = models.TextField(blank=True)
	exit_code = models.IntegerField()


class TestGeneratorError(models.Model):
	description = models.ForeignKey(RunErrorDescription)


class TestError(models.Model):
	PROGRAM_TYPES = (
		('v', 'validator'),
		('c', 'checker'),
	)
	program_type = models.CharField(max_length=1, choices=PROGRAM_TYPES)
	command_line = models.CharField(max_length=500)
	description = models.ForeignKey(RunErrorDescription)


class TestGeneratorTag(models.Model):
	name = models.CharField(max_length=50)
	value = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.name


class TestGenerator(models.Model):
	number = models.IntegerField()
	tags = models.ManyToManyField(TestGeneratorTag, related_name='+', blank=True)
	script = models.CharField(max_length=500)
	error = models.ForeignKey(TestGeneratorError, blank=True, null=True)

	def __str__(self):
		return self.script


class Test(models.Model):
	number = models.IntegerField()
	generator = models.ForeignKey(TestGenerator)
	error = models.ForeignKey(TestError, blank=True, null=True)

	def __str__(self):
		return str(number)


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
	possible_verdicts = models.ManyToManyField(Verdict, related_name='+')
	problem = models.ForeignKey('Problem')
	filename = models.CharField(max_length=256)
	path_or_stdin = models.CharField(max_length=64)
	path_or_stdout = models.CharField(max_length=64)

	def __str__(self):
		return str(self.problem) + ': solution ' + str(self.fname)
