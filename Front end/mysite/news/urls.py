__author__ = 'Work'

from django.conf.urls import url
from news.views import index, articles

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'articles/$', views.articles, name = 'articles'),
    url(r'summary/$', views.summary, name='summary'),
]