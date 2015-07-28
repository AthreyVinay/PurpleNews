import urllib.request
from bs4 import BeautifulSoup
import re
from newspaper import Article

import goslate

categories = ['news','opinion','business','money','sport',
              'lifestyle','arts','politics','culture']

urlb = 'http://www.bild.de'

categoryDetail = [{'name':'sport',
    'url':'http://www.bild.de/sport/startseite/sport/sport-home-15479124.bild.html',
     'keyword': '/sport/'},
                  {'name':'business',
    'url':'http://www.bild.de/geld/startseite/geld/home-15683376.bild.html',
     'keyword': '/geld/'},
                  {'name':'politics',
    'url':'http://www.bild.de/politik/startseite/politik/home-16804552.bild.html',
     'keyword': '/politik/'},
                  {'name':'lifestyle',
    'url':'http://www.bild.de/lifestyle/startseite/lifestyle/lifestyle-15478526.bild.html',
     'keyword': '/lifestyle/'},
                  ]

def getGermanNews(category):

    if category in categories:
        url = ''
        if category == 'sport':
            url = categoryDetail[0]['url']
            cate = categoryDetail[0]['keyword']

        if category =='business':
            url = categoryDetail[1]['url']
            cate = categoryDetail[1]['keyword']

        if category =='politics':
            url = categoryDetail[2]['url']
            cate = categoryDetail[2]['keyword']

        if category =='lifestyle':
            url = categoryDetail[3]['url']
            cate = categoryDetail[3]['keyword']



        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, from_encoding='utf8')

        article_list = []

        hotNews = soup.find_all('img')



        for i in hotNews:
            parent = i.parent
            a = parent.attrs
            # print(a)
            if 'href' in a:

                m = re.match(r"^%s" % cate,a['href'])
                if m is not None:

                    url = a['href']
                    articleUrl = urlb.__add__(url)
                    article_list.append(articleUrl)


        return article_list



def getGermanArticlese(url_list):

    germanArticles = []

    title = ''
    summary = ''
    articleUrl = ''
    imageUrl = ''

    for i in url_list:
        url = i


    # url = 'http://deportes.elpais.com/deportes/2015/07/21/actualidad/1437504468_097396.html'
        a = Article(url,language = 'de')

        a.download()
        a.parse()

        title = translateToEn(a.title)
        imageUrl = a.top_image
        summary = translateToEn(a.text[:1500])

        current_article_dict = {
                                    "title": title,
                                    # "description": summary,
                                    "articleUrl": url,
                                    "imageUrl": imageUrl
                                  }
        germanArticles.append(current_article_dict)



    return germanArticles


def translateToEn(text):

    gs = goslate.Goslate()
    result = gs.translate(text,'en')
    return result


# print (getGermanArticlese(getGermanNews('business')))

