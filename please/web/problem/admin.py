from django.contrib import admin
from problem.models import RunErrorDescription, TestGeneratorError,
                           TestError, TestGeneratorTag, TestGenerator, Test,
                           Tag, Solution, Verdict

admin.site.register(RunErrorDescription)
admin.site.register(TestGeneratorError)
admin.site.register(TestError)
admin.site.register(TestGeneratorTag)
admin.site.register(TestGenerator)
admin.site.register(Test)
admin.site.register(Tag)
admin.site.register(Solution)
admin.site.register(Verdict)
admin.site.register(Problem)