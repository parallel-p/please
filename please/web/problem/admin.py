from django.contrib import admin
from problem.models import *


for model in (RunErrorDescription, TestGeneratorError, TestError, TestGeneratorTag, TestGenerator, Test, Tag, Solution, Verdict):
	admin.site.register(model)

