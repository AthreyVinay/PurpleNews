from django.shortcuts import render
import tweepy
import yweather
import urllib.request
from bs4 import BeautifulSoup
import re
# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

auth = tweepy.OAuthHandler('DFuMLbEuenPTnrCfiPUwVuNHG', '2p6jAKwsull7vfDQkfjgm1TMQRyf0u2ciIP6vvhaXAlQztoVJ3')
auth.set_access_token('305656793-y7byCZEg8AaWB33U8s57khP5r6gFoiBuylNe5wR3', 'GD7OxNkz7kGzzRkE5dhV2KUnM2qbZCqABpU1w1BW2uFTG')
api = tweepy.API(auth)


def search(request):
    keyword=request.GET['keyword']
    tweets=[]
    tweet=api.search(keyword,'en')
    for t in tweet:
       tweets.append("@"+t.author.screen_name+":"+t.text)

    return render(request,'twse.html',{'tweets':tweets})

def trend(request):

    place=request.GET['place']
    client = yweather.Client()
    woeid=client.fetch_woeid(place)
    trends1 = api.trends_place(woeid)
    hashtags = [x['name'] for x in trends1[0]['trends'] if x['name'].startswith('#')]
    return render(request,'trends.html',{'hashtags':hashtags})


def getNewsByCategory(request):
    category=request.GET['category']
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
        info_dict = {'j1':j1,'j2':j2,'t1':t1,'d1':d1}

        return render(request,'news.html',{'info_dict':info_dict})



from apiclient.discovery import build
#from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDeTeuxawKX24ZhTnJYz_yVvXMhL2CEIw0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
def youtube_search(request):
    to_search=request.GET['ysearch']
   #language = lan
    argparser.add_argument("--q", help="Search term", default=to_search)
    #argparser.add_argument("--order",help="order",default='relevance')
   #argparser.add_argument("--relevanceLanguage",help="relevanceLanguage",default=language)
    argparser.add_argument("--max-results", help="Max results", default=5)
    options = argparser.parse_args()

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
    search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    #order=options.order,
    #relevanceLanguage=options.relevanceLanguage,
    maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("https://www.youtube.com/embed/"+"%s" % (search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))

    return render(request,'youtube.html',{'videos':videos})
  #print ("Channels:\n", "\n".join(channels), "\n")
  #print ("Playlists:\n", "\n".join(playlists), "\n")



