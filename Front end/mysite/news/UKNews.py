import urllib.request
from bs4 import BeautifulSoup
import re

import nltk
from nltk.corpus import brown

categories = ['news','opinion','business','money','sport',
              'lifestyle','arts','politics','culture']

urlb = 'http://www.telegraph.co.uk'




class UKarticles:

    def getNewsByCategory(category):

        if category in categories:

            if category == 'business':
                category = 'finance/businesslatestnews'

            url = urlb.__add__('/' + category + '/')

            content = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(content, from_encoding='GB18030')

            article_list = []

            if category == 'sport' or category == 'finance/businesslatestnews' or category == 'politics' or category == 'lifestyle':

                # hotNews = soup.find_all('div', {'class', 'summary'})
                hotNews = soup.find_all(class_=re.compile('headlineImage'))
                # print(hotNews)

                for i in hotNews:

                    title = ''
                    summary = ''
                    articleUrl = ''
                    imageUrl = ''
                    keywords = []

                    # title
                    j = i.find('h3')
                    # print(j)
                    if j is not None:

                        title = j.a.text
                        Url = j.a['href']
                        articleUrl = urlb.__add__(Url)
                        if articleUrl is not None:

                            # news image url
                            # t = i.find('div', {'class', 'piccentre'})
                            t = i.find(class_=re.compile('containerdiv'))
                            if t is not None:

                               # image url
                               imageUrl  = t.img['src']

                               #  sumarry
                               su = i.find('div', {'class', 'labelAbstract'})
                               if su is not None:
                                 summary = su.a.text


                                 current_article_dict = {
                                    "title": title,
                                    "description": summary,
                                    "articleUrl": articleUrl,
                                    "imageUrl": imageUrl
                                  }
                                 article_list.append(current_article_dict)



                # for i in article_list:
                #         if len(i.get("description"))<3 or i.get("description") is None \
                #                 or i.get("title") is None or len(i.get("title"))<3:
                #             article_list.remove(i)

                # for i in article_list:
                #     for j in article_list:
                #         if i.get("title") == j.get("title"):
                #             article_list.remove(j)

                return article_list




# doc = UKarticles.getNewsByCategory('politics')
# for i in doc:
#
#          print(i)

