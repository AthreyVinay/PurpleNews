from django.shortcuts import render
import tweepy
import yweather
import urllib.request
from bs4 import BeautifulSoup
import re
import pywapi
from .ys import youtube_search
# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

auth = tweepy.OAuthHandler('DFuMLbEuenPTnrCfiPUwVuNHG', '2p6jAKwsull7vfDQkfjgm1TMQRyf0u2ciIP6vvhaXAlQztoVJ3')
auth.set_access_token('305656793-y7byCZEg8AaWB33U8s57khP5r6gFoiBuylNe5wR3', 'GD7OxNkz7kGzzRkE5dhV2KUnM2qbZCqABpU1w1BW2uFTG')
api = tweepy.API(auth)


def search(request):
    keyword=request.GET['keyword']

    tweet=api.search(keyword,'en')

    return render(request,'twse.html',{'tweets':tweet})

def trend(request):

    place=request.GET['place']
    client = yweather.Client()
    woeid=client.fetch_woeid(place)
    trends1 = api.trends_place(woeid)
    hashtags = [x['name'] for x in trends1[0]['trends'] if x['name'].startswith('#')]
    tws=[]
    for h in hashtags:
        tweet=api.search(h,'en')
        for t in tweet:
            tws.append("@"+t.author.screen_name+":"+t.text)
    return render(request,'trends.html',{'hashtags':hashtags,'tweets':tws})


def getNewsByCategory(request):
    result = pywapi.get_weather_from_yahoo('EIXX0014', 'metric')
    category=request.GET['category']
    place=request.GET['cp']
    client = yweather.Client()
    woeid=client.fetch_woeid(place)
    trends1 = api.trends_place(woeid)
    hashtags = [x['name'] for x in trends1[0]['trends'] if x['name'].startswith('#')]
    categories = ['news','opinion/','business','money','sport',
              'life','arts','puzzles']


    urlb = 'http://www.thetimes.co.uk/tto'
    j1=[]
    j2=[]
    t1=[]
    d1=[]


    if category in categories:
        url = urlb.__add__('/' + category + '/')
            # print('url is %s',url)

        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, from_encoding='GB18030')

        hotNews = soup.find_all(class_=re.compile('article-'))

        for i in hotNews:

            j = i.find('h2')
            if j is not None:
                j1.append(j.text)
                j2.append(j.a['href'])

                # news contents
            t = i.find('div', {'class', 'ellipsis'})

            if t is not None:
                t1.append(t.text)

                # news date
            d = i.find('div', {'class', 'f-regular-update'})
            if d is not None:
                d1.append(d.text)
        else:
            print('not a valid category')

        data=[]
        a = 0
        while a < len(j1):
            data.append({'ji':j1[a],'j2':j2[a],"da":d1[a],'t1':t1[a]})
        info_dict = {'j1':j1,'j2':j2,'t1':t1,'d1':d1}

        return render(request,'news.html',{'info_dict':info_dict,'hashtages':hashtags,'weather':result,'data':data})


def ysearch(request):

    sysearch =  None

    if request.method == 'GET':
       sysearch = request.GET['youwords']
         # print(ysearch(sysearch))
    return render(request,'youtube.html',{'videos':youtube_search(sysearch)})

def article(request):

    return render(request, 'article.html')