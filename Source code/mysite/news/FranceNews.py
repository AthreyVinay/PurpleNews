import urllib.request
from bs4 import BeautifulSoup
import re



# Global defines
sportsFeedUrl = "http://www.thelocal.fr/page/view/sport"
businessFeedUrl = "http://www.thelocal.fr/page/view/money"
politicsFeedUrl = "http://www.thelocal.fr/page/view/politics"
entertainmentFeedUrl = "http://www.thelocal.fr/page/view/travel"
requestHeaders = {'User-agent': 'Mozilla/5.0'}

def getFrenchArticles(category):

    downloadUrl = ""

    if category == "sports":
        downloadUrl = sportsFeedUrl
    elif category == "politics":
        downloadUrl = politicsFeedUrl
    elif category == "business":
        downloadUrl = businessFeedUrl
    elif category == 'entertainment':
        downloadUrl = entertainmentFeedUrl

    content = urllib.request.urlopen(downloadUrl).read()
    soup = BeautifulSoup(content, from_encoding='utf8')

    newsArray = []
    for newsArticle in soup.findAll("div", { "class" : "newsSummary" }):

        newsTitle = newsArticle.find("div", {"class": "small"})

        if newsTitle != None:
            newsTitle = newsTitle.get_text()
        else:
            newsTitle = ""

        description = newsArticle.find("p").get_text().strip()
        # np_extractor = NPExtractor(description)
        # result = np_extractor.extract()

        current_article_dict = {
                "title": newsTitle,
                "description": description,
                "articleUrl": newsArticle.find("a")["href"],
                "keywords": ""
            }

        newsArray.append(current_article_dict)


    return newsArray


# getFrenchArticles("business")
