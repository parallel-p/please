from .models import Contest, ContestProblem, ContestNode, Category
from django.contrib import admin

admin.site.register(Contest)
admin.site.register(ContestProblem)
admin.site.register(ContestNode)
admin.site.register(Category)