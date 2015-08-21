__author__ = 'Work'

from django.conf.urls import url
from news.views import index, articles, summary, about, contact
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^$', csrf_exempt(index.as_view())),
    url(r'articles/$', csrf_exempt(articles.as_view())),
    url(r'summary/$', csrf_exempt(summary.as_view())),
    url(r'about/$', csrf_exempt(about.as_view())),
    url(r'contact/$', csrf_exempt(contact.as_view())),
]