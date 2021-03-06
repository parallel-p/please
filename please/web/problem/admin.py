from django.contrib import admin
from problem.models import (RunErrorDescription, TestGeneratorError,
                           TestError, TestGeneratorTag, TestGenerator, Test,
                           ProblemTag, Solution, Verdict, Problem, WellDone, TestResult)

admin.site.register(RunErrorDescription)
admin.site.register(TestGeneratorError)
admin.site.register(TestError)
admin.site.register(TestGeneratorTag)
admin.site.register(TestGenerator)
admin.site.register(Test)
admin.site.register(ProblemTag)
admin.site.register(Solution)
admin.site.register(Verdict)
admin.site.register(Problem)
admin.site.register(WellDone)
admin.site.register(TestResult)
