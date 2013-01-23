from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin


urlpatterns = patterns('',
    url(r's/(?P<id>\d+)$', 'contest.views.contest.index', name = 'contest'), 
    url(r's/(?P<id>\d+)/problems/delete/(?P<problem_id>\d+)$', 'contest.views.contest.delete_problem', name='delete'),
    url(r's/(?P<id>\d+)/statement/view$', 'contest.views.contest.view_statement', name="view_contest_statement"),
    url(r's/$', 'contest.views.contests.index'),
    url(r'/create/$', 'contest.views.contests.create'),
    url(r'/add/$', 'contest.views.contests.add'),
    url(r'/add_tree/$', 'contest.views.contests.add_tree'),
    url(r'/import/polygon/$', 'contest.views.contests.import_from_polygon'),
    url(r's/tree/$', 'contest.views.tree.show_categories'),
    )
