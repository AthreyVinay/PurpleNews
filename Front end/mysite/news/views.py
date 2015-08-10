from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from tweepy.streaming import json
from .models import Article
import forecastio
from news.twitter import search
from news.UKNews import getNewsByCategory
from news.articleManager2 import get_article_list
from news.weather_forecast import weather_forecast
from news.ys import ysearch


# Create your views here.

class index(View):

    def get(self, request):
        return self.get_forecast(request)

    def get_forecast(self, request):
        weather_ireland = weather_forecast(53.3442,6.2675)
        weather_UK = weather_forecast(51.5000, 0.1167)

        context = {"Ireland_weather": weather_ireland, "UK_weather": weather_UK}
        return render(request, 'news/index.html', context)

class articles(View):

    def get(self, request):
        country = request.POST['country']

        return render(request, 'news/articles.html')

    def post(self, request):
        if(self.request.is_ajax()):
            return self.ajax(request)
        else:
            country = request.POST['country']

            if country == "United Kingdom":
                business = getNewsByCategory("business")[:5]
                sport = getNewsByCategory("sport")[:5]
                politics = getNewsByCategory("politics")[:5]
                lifestyle = getNewsByCategory("lifestyle")[:5]

                context = {"country": country, "business": business, "sport" : sport, "politics": politics, "lifestyle" : lifestyle}

            elif country == "Ireland":
                business = get_article_list("business")[:5]
                sport = get_article_list("sports")[:5]
                politics = get_article_list("politics")[:5]
                lifestyle = get_article_list("lifestyle")[:5]

                context = {"country": country, "business": business, "sport": sport, "politics": politics, "lifestyle": lifestyle}

            return render(request, "news/articles.html",context)

    def ajax(self, request):
        category = request.POST.get('category', '')
        country = request.POST.get('country', '')
        articles = Article.objects.filter(country=country, category=category)
        titles = []
        for article in articles:
            titles.append(article.title)

        json_articles = serializers.serialize("json", articles)

        context = {"success": True, "category" : category,"country" :country, "titles" : titles}
        return HttpResponse(json.dumps(context), content_type='application/json')

class summary(View):

    def get(self, request):
        tweets = search("Greek crisis")
        keywords = ["Greek crisis", "Sky news", "Greek crisis", "CNN"]
        videos = ysearch(keywords)
        article_title = "Greek crisis"
        context = {"tweets": tweets, "videos1" : videos[0], "videos2": videos[1], "article_title": article_title}
        return render(request, 'news/summary.html', context)

    def post(self, request):
        tweets = search("Greek crisis")
        keywords = ["Greek crisis", "Sky news", "Greek crisis", "CNN"]
        videos = ysearch(keywords)
        article_title = request.POST.get('article_title','')
        context = {"tweets": tweets, "videos1" : videos[0], "videos2": videos[1], "article_title": article_title}
        return render(request, 'news/summary.html', context)