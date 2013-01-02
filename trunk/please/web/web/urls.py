from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^problems/', 'problem.views.problems_search'),
    url(r'^problem/(?P<id>\d+)/materials/edit/$', 'problem.views.edit_problem_materials'),
    url(r'^problem/confirmation', TemplateView.as_view(template_name='problem_edit_success.html')),
)
