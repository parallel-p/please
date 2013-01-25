from django.db import models
from please.web.problem.models import Problem
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    order = models.IntegerField(max_length=4)

    def __str__(self):
        return self.name
        
    class MPTTMeta:
        order_insertion_by = ['order']


class Contest(models.Model):
    name = models.CharField(blank=True, max_length=256)
    path = models.CharField(max_length=1000)

    ID_METHODS = (('d', 'default'), 
                  ('a', 'alpha'), 
                  ('n', 'numeric'), 
                 )
    id_method =  models.CharField(max_length=1, choices=ID_METHODS)
    
    statement_name = models.CharField(blank=True, max_length=1000)
    statement_location = models.CharField(blank=True, max_length=1000)
    statement_date = models.CharField(blank=True, max_length=1000)
    statement_template = models.CharField(blank=True, max_length=1000, default='contest.tex')
    problems = models.ManyToManyField(Problem, through='ContestProblem')
    tree_nodes = models.ManyToManyField(Category, through='ContestNode')

    def __str__(self):
        return self.name

class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest)
    problem = models.ForeignKey(Problem)
    order = models.IntegerField()
    id_in_contest = models.CharField(max_length=256, blank=True, default='')

    def __str__(self):
        return '{} - {}'.format(self.contest, self.problem)
    
    class Meta:
        ordering = ['order',]


class ContestNode(models.Model):
    contest = models.ForeignKey(Contest)
    node = models.ForeignKey(Category)
    order = models.IntegerField()
    
    def __str__(self):
        return '{} - {}'.format(self.contest, self.node)
    
    class Meta:
        ordering = ['order',]

