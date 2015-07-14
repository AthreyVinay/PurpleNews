from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from .models import Message
from django.views.generic import View
from news.UKNews import UKarticles
from news.ys import ysearch
from news.twitter import search
from django.views.generic import TemplateView
from news.articleManager2 import get_article_list_2
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from .models import Article, Tweet

# Create your views here.

def index(request):
        return render(request, 'news/index.html')


@csrf_exempt
def articles(request):

        country = request.POST['country']
        articles = Article.objects.filter(country=country)

        context = {"articles":articles}
        return render(request, "news/articles.html", context)


def summary(request):
    try:
        text = request.POST['text']
    except MultiValueDictKeyError:
        text = False

    #art_title = request.POST.get('title', "false")

    context = {"text":text}
    return render(request, 'news/summary.html', context)