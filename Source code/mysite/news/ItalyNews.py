import urllib.request
from bs4 import BeautifulSoup
import re
from newspaper import Article

import goslate


categories = ['news','opinion','business','money','sport',
              'lifestyle','arts','politics','culture']

urlb = 'http://www.corriere.it'

categoryDetail = [{'name':'sport',
    'url':'http://www.corriere.it/sport/',
     'keyword': 'http://www.corriere.it/sport/'},
                  {'name':'business',
    'url':'http://www.corriere.it/economia/',
     'keyword': 'http://www.corriere.it/economia/'},
                  {'name':'politics',
    'url':'http://www.corriere.it/scuola/index.shtml',
     'keyword': 'http://www.corriere.it/scuola/'},
                  {'name':'lifestyle',
    'url':'http://www.corriere.it/la-lettura/',
     'keyword': 'http://www.corriere.it/foto-gallery/'},
                  ]

def getItalyNews(category):

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
                    # articleUrl = urlb.__add__(url)
                    articleUrl =url
                    # for business politics
                    article_list.append(articleUrl)

        # print(article_list)


        return article_list



def getItalyArticlese(url_list):

    ItalyArticles = []

    title = ''
    summary = ''
    articleUrl = ''
    imageUrl = ''


    for i in url_list:
        url = i


    # url = 'http://deportes.elpais.com/deportes/2015/07/21/actualidad/1437504468_097396.html'
        a = Article(url,language = 'it')

        a.download()
        a.parse()

        title = translateToEn(a.title)
        imageUrl = a.top_image
        summary = translateToEn(a.text[:1500])


        current_article_dict = {
                                    "title": title,
                                    "description": summary,
                                    "articleUrl": url,
                                    "imageUrl": imageUrl,

                                  }
        ItalyArticles.append(current_article_dict)



    return ItalyArticles


def translateToEn(text):

    gs = goslate.Goslate()
    result = gs.translate(text,'en')
    return result


# for i in getItalyArticlese(getItalyNews('lifestyle')):
#     print(i)

