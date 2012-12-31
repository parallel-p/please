from django.contrib import admin
from problem.models import *
from traceback import print_tb

for cls in (Tag, Solution, Verdict):
	admin.site.register(cls)