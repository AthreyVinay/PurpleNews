__author__ = 'Work'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),  # question id changed to 'pk'
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),  # ****
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]