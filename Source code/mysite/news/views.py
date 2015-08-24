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

from news.GermanNews import getGermanNews, getGermanArticlese
from news.SpainNews import getSpainNews, getSpainArticlese
from news.ItalyNews import getItalyArticlese, getItalyNews
from news.FranceNews import getFrenchArticles

from news.keywords import NPExtractor



# Create your views here.

class index(View):

    def get(self, request):
        # Article.objects.all().delete()
        return self.get_forecast(request)

    def get_forecast(self, request):
        weather_ireland = weather_forecast(53.3442, 6.2675)
        weather_UK = weather_forecast(51.5000, 0.1167)
        weather_spain = weather_forecast(40.4333, 3.7)
        weather_germany = weather_forecast(52.5167, 13.3833)
        weather_italy = weather_forecast(41.90000, 12.4833)
        weather_france = weather_forecast(47.0, 2.0)

        context = {"Ireland_weather": weather_ireland, "UK_weather": weather_UK, "Spain_weather": weather_spain,
                   "Germany_weather": weather_germany, "Italy_weather": weather_italy, "France_weather": weather_france}
        return render(request, 'news/index.html', context)



class articles(View):

    def get(self, request):
        # country = request.POST['country']
        #
        # return render(request, 'news/articles.html')
        business = Article.objects.filter(category="business")
        sport = Article.objects.filter(category="sport")
        politics = Article.objects.filter(category="politics")
        lifestyle = Article.objects.filter(category="lifestyle")
        context = {"business": business, "sport": sport, "politics": politics, "lifestyle": lifestyle}

        return render(request, 'news/articles.html', context)

    def post(self, request):
        country = request.POST['country']

        print(country)

        if country == "United Kingdom":
            business = getNewsByCategory("business")[:5]
            sport = getNewsByCategory("sport")[:5]
            politics = getNewsByCategory("politics")[:5]
            lifestyle = getNewsByCategory("lifestyle")[:5]

            for index in [0, 1, 2, 3]:
                new_entry = Article(title=business[index]["title"], summary=business[index]["description"],
                                    country=country, category="business")
                new_entry.save()
                new_entry = Article(title=sport[index]["title"], summary=sport[index]["description"], country=country,
                                    category="sport")
                new_entry.save()
                new_entry = Article(title=politics[index]["title"], summary=politics[index]["description"],
                                    country=country, category="politics")
                new_entry.save()
                new_entry = Article(title=lifestyle[index]["title"], summary=lifestyle[index]["description"],
                                    country=country, category="lifestyle")
                new_entry.save()

            context = {"country": country, "business": business, "sport": sport, "politics": politics,
                       "lifestyle": lifestyle}

        elif country == "Ireland":
            business = get_article_list("business")[:5]
            sport = get_article_list("sports")[:5]
            politics = get_article_list("politics")[:5]
            lifestyle = get_article_list("lifestyle")[:5]

            for index in [0, 1, 2, 3, 4]:
                new_entry = Article(title=business[index]["title"], summary=business[index]["description"],
                                    country=country, category="business")
                new_entry.save()
                new_entry = Article(title=sport[index]["title"], summary=sport[index]["description"], country=country,
                                    category="sport")
                new_entry.save()
                new_entry = Article(title=politics[index]["title"], summary=politics[index]["description"],
                                    country=country, category="politics")
                new_entry.save()
                new_entry = Article(title=lifestyle[index]["title"], summary=lifestyle[index]["description"],
                                    country=country, category="lifestyle")
                new_entry.save()

            context = {"country": country, "business": business, "sport": sport, "politics": politics,
                       "lifestyle": lifestyle}

        elif country == "Germany":
            business = getGermanArticlese(getGermanNews("business"))[:5]
            sport = getGermanArticlese(getGermanNews("sport"))[:5]
            politics = getGermanArticlese(getGermanNews("politics"))[:5]
            lifestyle = getGermanArticlese(getGermanNews("lifestyle"))[:5]

            for index in [0, 1, 2, 3, 4]:
                new_entry = Article(title=business[index]["title"], summary=business[index]["description"],
                                    country=country, category="business")
                new_entry.save()
                new_entry = Article(title=sport[index]["title"], summary=sport[index]["description"], country=country,
                                    category="sport")
                new_entry.save()
                new_entry = Article(title=politics[index]["title"], summary=politics[index]["description"],
                                    country=country, category="politics")
                new_entry.save()
                new_entry = Article(title=lifestyle[index]["title"], summary=lifestyle[index]["description"],
                                    country=country, category="lifestyle")
                new_entry.save()

            context = {"country": country, "business": business, "sport": sport, "politics": politics,
                       "lifestyle": lifestyle}

        elif country == "Spain":
            business = getSpainArticlese(getSpainNews("business"))[:5]
            sport = getSpainArticlese(getSpainNews("sport"))[:5]
            politics = getSpainArticlese(getSpainNews("politics"))[:5]
            lifestyle = getSpainArticlese(getSpainNews("lifestyle"))[:5]

            for index in [0, 1, 2, 3, 4]:
                new_entry = Article(title=business[index]["title"], summary=business[index]["description"],
                                    country=country, category="business")
                new_entry.save()
                new_entry = Article(title=sport[index]["title"], summary=sport[index]["description"], country=country,
                                    category="sport")
                new_entry.save()
                new_entry = Article(title=politics[index]["title"], summary=politics[index]["description"],
                                    country=country, category="politics")
                new_entry.save()
                new_entry = Article(title=lifestyle[index]["title"], summary=lifestyle[index]["description"],
                                    country=country, category="lifestyle")
                new_entry.save()

            context = {"country": country, "business": business, "sport": sport, "politics": politics,
                       "lifestyle": lifestyle}

        elif country == "Italy":
            business = getItalyArticlese(getItalyNews("business"))[:5]
            sport = getItalyArticlese(getItalyNews("sport"))[:5]
            politics = getItalyArticlese(getItalyNews("politics"))[:5]
            lifestyle = getItalyArticlese(getItalyNews("lifestyle"))[:5]

            for index in [0, 1, 2, 3, 4]:
                new_entry = Article(title=business[index]["title"], summary=business[index]["description"],
                                    country=country, category="business")
                new_entry.save()
                new_entry = Article(title=sport[index]["title"], summary=sport[index]["description"], country=country,
                                    category="sport")
                new_entry.save()
                new_entry = Article(title=politics[index]["title"], summary=politics[index]["description"],
                                    country=country, category="politics")
                new_entry.save()
                new_entry = Article(title=lifestyle[index]["title"], summary=lifestyle[index]["description"],
                                    country=country, category="lifestyle")
                new_entry.save()

            context = {"country": country, "business": business, "sport": sport, "politics": politics,
                       "lifestyle": lifestyle}

        elif country == "France":
            # business = getFranceArticlese(getFranceNews("business"))[:5]
            # sport = getFranceArticlese(getFranceNews("sport"))[:5]
            # politics = getFranceArticlese(getFranceNews("politics"))[:5]
            # lifestyle = getFranceArticlese(getFranceNews("lifestyle"))[:5]

            business = getFrenchArticles("business")[:5]
            sport = getFrenchArticles("sports")[:5]
            politics = getFrenchArticles("politics")[:5]
            lifestyle = getFrenchArticles("entertainment")[:5]

            for index in [0, 1, 2, 3, 4]:
                new_entry = Article(title=business[index]["title"], summary=business[index]["description"],
                                    country=country, category="business")
                new_entry.save()
                new_entry = Article(title=sport[index]["title"], summary=sport[index]["description"], country=country,
                                    category="sport")
                new_entry.save()
                new_entry = Article(title=politics[index]["title"], summary=politics[index]["description"],
                                    country=country, category="politics")
                new_entry.save()
                new_entry = Article(title=lifestyle[index]["title"], summary=lifestyle[index]["description"],
                                    country=country, category="lifestyle")
                new_entry.save()

            context = {"country": country, "business": business, "sport": sport, "politics": politics,
                       "lifestyle": lifestyle}

        return render(request, "news/articles.html", context)


# class summary(View):
#
#     def get(self, request):
#         tweets = search("Greek crisis")
#         keywords = ["Greek crisis", "Sky news", "Greek crisis", "CNN"]
#         videos = ysearch(keywords)
#         article_title = "Greek crisis"
#         context = {"tweets": tweets, "videos1" : videos[0], "videos2": videos[1], "article_title": article_title}
#         return render(request, 'news/summary.html', context)
#
#     def post(self, request):
#         tweets = search("Greek crisis")
#         keywords = ["Greek crisis", "Sky news", "Greek crisis", "CNN"]
#         videos = ysearch(keywords)
#         article_title = request.POST.get('article_title','')
#         context = {"tweets": tweets, "videos1" : videos[0], "videos2": videos[1], "article_title": article_title}
#         return render(request, 'news/summary.html', context)


class summary(View):
    def get(self, request):
        return render(request, 'news/summary.html')

    def post(self, request):
        article_title = request.POST.get('article_title', 'false')
        # article = Article.objects.get(title=article_title)
        article = Article.objects.filter(title=article_title)
        description = article[0].summary
        np_extractor = NPExtractor(article_title)
        keywords = np_extractor.extract()
        tweets = search(keywords)

       # print("The title: " + article_title)

        keywords.append("Sky news")
        video1 = ysearch(keywords)
        keywords.pop()
        keywords.append("RT")
        video2 = ysearch(keywords)
        keywords.pop()
        keywords.append("CNN")
        video3 = ysearch(keywords)
        keywords.pop()
        keywords.append("Al jazeera")
        video4 = ysearch(keywords)

        context = {"tweets": tweets, "article_title": article_title, "description": description, "keywords": keywords,
                   "video1": video1, "video2": video2,"video3": video3, "video4": video4}
        return render(request, 'news/summary.html', context)


class about(View):
    def get(self, request):
        return render(request, 'news/about.html')


class contact(View):
    def get(self, request):
        return render(request, 'news/contact.html')