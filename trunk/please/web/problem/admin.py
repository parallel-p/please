from django.contrib import admin
from problem.models import Tag, Solution, Verdict

for cls in (Tag, Solution, Verdict):
	admin.site.register(cls)