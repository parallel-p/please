from django.db import models
from please.web.problem.models import Problem

# Create your models here.

class Contest(models.Model):
    name = models.CharField(max_length=256)

    ID_METHODS = (('d', 'default'), 
                  ('a', 'alpha'), 
                  ('n', 'numeric'), 
                 )
    id_method =  models.CharField(max_length=1, choices=ID_METHODS)
    
    statement_name = models.CharField(max_length=1000)
    statement_location = models.CharField(max_length=1000)
    statement_date = models.CharField(max_length=1000)
    statement_template = models.CharField(max_length=1000)
    problems = models.ManyToManyField(Problem, through='ContestProblem')

    def __str__(self):
        return self.name

class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest)
    problem = models.ForeignKey(Problem)
    order = models.IntegerField()
    id_in_contest = models.CharField(max_length=256)

    def __str__(self):
        return '{} - {}'.format(self.contest, self.problem)
    