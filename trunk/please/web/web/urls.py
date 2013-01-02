from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^problems/', 'problem.views.problems_search_by_tag'),
    url(r'^problem/(?P<id>\d+)/todo/$', 'problem.views.todo'),
    url(r'^problem/(?P<id>\d+)/materials/edit/$', 'problem.views.edit_problem_materials'),
    url(r'^problem/(?P<id>\d+)/files/upload/main$', 'problem.views.add_problem_files', name='file_upload'),
    url(r'^problem/(?P<id>\d+)/files/upload/additional$', 'problem.views.add_user_files()'),
    url(r'^problem/(?P<id>\d+)/solutions/add/$', 'problem.views.add_solution'),
    url(r'^problem/confirmation$', TemplateView.as_view(template_name='problem_edit_success.html')),
    url(r'^problem/create', 'problem.views.create_problem')
)
