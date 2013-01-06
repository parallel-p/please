from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^problems/$', 'problem.views.problems.index'),
    url(r'^$', 'problem.views.problems.index'),
    url(r'^problems/add/$', 'problem.views.problems.add'),
    url(r'^problems/add-tree/$', 'problem.views.problems.add_tree'),
    url(r'^problems/create/$', 'problem.views.problems.create'),
    url(r'^problems/import/polygon/$', 'problem.views.problems.import_from_polygon', name='polygon-import'),
    url(r'^problems/confirmation/$', TemplateView.as_view(template_name='problem_edit_success.html')),

    url(r'^problems/(?P<id>\d+)/materials/statement/generate/$', 'problem.views.materials.gen_statement', name="gen_statement"),
    url(r'^problems/(?P<id>\d+)/files/upload/additional$', 'problem.views.files.upload_additional_view', name='additional_upload'),
    url(r'^problems/(?P<id>\d+)/tags/$', 'problem.views.tags.edit_tags_view', name='edit_tags'),
    url(r'^problems/(?P<problem_id>\d+)/tests/(?P<test_name>\d+(\.a)?)/$', 'problem.views.problems.show_test'),
    url(r'^problems/(?P<problem_id>\d+)/build_all/$', 'problem.views.problem.build_all', name='build-all'),

    url(r'^problems/(?P<id>\d+)/settings/$', 'problem.views.problem.settings'),
    url(r'^problems/(?P<id>\d+)/$', 'problem.views.problem.settings'),
    url(r'^problems/(?P<id>\d+)/solutions/$', 'problem.views.problem.solutions'),
    url(r'^problems/(?P<id>\d+)/statements/$', 'problem.views.problem.statements', name='problem_statement'),
    url(r'^problems/(?P<id>\d+)/tests/$', 'problem.views.problem.tests'),
)
