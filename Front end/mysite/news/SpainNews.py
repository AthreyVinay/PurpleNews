

#translate to english using google translation api
# import goslate
#
# def translateToEn(text):
#
#     gs = goslate.Goslate()
#     result = gs.translate(text,'en')
#     return result
#     print(result)
#
#
# translateToEn('Cuando Luis Suárez fichó por el Barcelona el verano pasado tuvo que esperar en boxes hasta finales de octubre.')


# from newspaper import Article
#
# def example():
#     url = 'http://deportes.elpais.com/deportes/2015/07/21/actualidad/1437504468_097396.html'
#     a = Article(url,language = 'de')
#
#     a.download()
#     a.parse()
#
#     print(a.text[:1500])
#
#     print(a.title)
#     print(a.top_image)
#
# example()

# import newspaper
#
# de_paper = newspaper.build('http://www.bild.de/politik/startseite/politik/home-16804552.bild.html')
#
# for article in de_paper.articles:
#     print(article.url)


import urllib.request
from bs4 import BeautifulSoup
import re
from newspaper import Article

import goslate

categories = ['news','opinion','business','money','sport',
              'lifestyle','arts','politics','culture']

urlb = 'http://politica.elpais.com'

categoryDetail = [{'name':'sport',
    'url':'http://deportes.elpais.com',
     'keyword': '/deportes/'},
                  {'name':'business',
    'url':'http://economia.elpais.com/',
     'keyword': '/economia/'},
                  {'name':'politics',
    'url':'http://politica.elpais.com',
     'keyword': '/politica/'},
                  {'name':'lifestyle',
    'url':'http://cultura.elpais.com/',
     'keyword': '/cultura/'},
                  ]

def getSpainNews(category):

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

        # print(article_list)
        return article_list



def getSpainArticlese(url_list):

    spainArticles = []

    title = ''
    summary = ''
    articleUrl = ''
    imageUrl = ''

    for i in url_list:
        url = i


    # url = 'http://deportes.elpais.com/deportes/2015/07/21/actualidad/1437504468_097396.html'
        a = Article(url,language = 'es')

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
        spainArticles.append(current_article_dict)



    return spainArticles


def translateToEn(text):

    gs = goslate.Goslate()
    result = gs.translate(text,'en')
    return result


# print (getSpainArticlese(getSpainNews('business')))


