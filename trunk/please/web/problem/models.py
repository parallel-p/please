from django.db import models


class ProblemTag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)


class WellDone(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)


class Problem(models.Model):
    path = models.CharField(max_length=256)

    name = models.CharField(max_length=64, blank=True)
    short_name = models.CharField(max_length=64)
    tags = models.ManyToManyField(ProblemTag, blank=True)

    input = models.CharField(max_length=64, default="stdin")
    output = models.CharField(max_length=64, default="stdout")
    time_limit = models.FloatField(default=1.0)
    memory_limit = models.IntegerField(default=128 * 1024 * 1024)

    checker_path = models.CharField(max_length=256, default="")
    validator_path = models.CharField(max_length=256, default="")
    main_solution = models.OneToOneField('Solution', related_name='problem+', blank=True, null=True)

    statement_path = models.CharField(max_length=256, default="")
    description_path = models.CharField(max_length=256, default="")
    analysis_path = models.CharField(max_length=256, default="")

    hand_answer_extension = models.CharField(max_length=64, default="")

    well_done_test = models.ManyToManyField(WellDone, related_name='well_done_test+', blank=True)
    well_done_answer = models.ManyToManyField(WellDone, related_name='well_done_answer+', blank=True)

    def __str__(self):
        """
        Human readable representainon.
        >>> str(Problem(short_name="abc"))
        'abc'
        """
        return str(self.short_name)


class RunErrorDescription(models.Model):
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    exit_code = models.IntegerField()

    def is_ok(self):
        """
        >>> RunErrorDescription(exit_code=0).is_ok()
        True
        >>> RunErrorDescription(exit_code=1).is_ok()
        False
        """
        return self.exit_code == 0


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
        """
        >>> str(TestGeneratorTag(name="abc", value="abcd"))
        'abc=abcd'
        """
        return '{}={}'.format(self.name, self.value) if self.value else str(self.name)


class TestGenerator(models.Model):
    line_number = models.IntegerField()
    tags = models.ManyToManyField(TestGeneratorTag, blank=True)
    script = models.CharField(max_length=500)
    error = models.ForeignKey(TestGeneratorError, blank=True, null=True)

    def __str__(self):
        return str(self.script)


class Test(models.Model):
    test_number = models.IntegerField()
    generator = models.ForeignKey(TestGenerator)
    error = models.ForeignKey(TestError, blank=True, null=True)

    def __str__(self):
        return str(self.test_number)


class Verdict(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return str(self.name)


class Solution(models.Model):
    expected_verdicts = models.ManyToManyField(Verdict, related_name='expected_verdicts+')
    possible_verdicts = models.ManyToManyField(Verdict, related_name='possible_verdicts+', blank=True)
    problem = models.ForeignKey(Problem)
    path = models.CharField(max_length=256)
    input = models.CharField(max_length=64, blank=True, null=True)
    output = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return '{}@{}'.format(self.path, self.problem)
