# coding=UTF-8
# #-------------------------------------------------------------------------------
# Name:        	getNewsArticles
# Purpose:		Get news article titles from IrishTimes
#
# Author:      	SUNHSIV
#
# Created:
# Copyright:   	(c)sunhsiv
# Licence:
# #-------------------------------------------------------------------------------

import nltk
from nltk.corpus import brown
from bs4 import BeautifulSoup
import urllib3
import xml.etree.ElementTree as et

#from newspaper import Article

# Global defines
worldFeedUrl = "http://www.irishtimes.com/cmlink/irishtimesworldfeed-1.1321046"
sportsFeedUrl = "http://www.irishtimes.com/cmlink/the-irish-times-sport-1.1319194"
businessFeedUrl = "http://www.irishtimes.com/cmlink/the-irish-times-business-1.1319195"
politicsFeedUrl = "http://www.irishtimes.com/cmlink/irish-times-politics-rss-1.1315953"
entertainmentFeedUrl = "http://www.irishtimes.com/cmlink/the-irish-times-life-style-1.1319214"
requestHeaders = {'User-agent': 'Mozilla/5.0'}

#   Class to parse XML data from Irish Times and HTML parser

#   Method: Download list of articles with a thumbnail image
    #   The method will return a list with each item having link to thumbnail image and text with artitle headline
def get_article_list(category_type):

    download_link = '`'

    if category_type == "sports":
        download_link = sportsFeedUrl
    elif category_type == "business":
        download_link = businessFeedUrl
    elif category_type == "politics":
        download_link = politicsFeedUrl
    elif category_type == "lifestyle":
        download_link = entertainmentFeedUrl

    try:

        http = urllib3.PoolManager()
        response = http.request('GET', download_link)
        r_data = response.data

        tree = et.ElementTree(et.fromstring(r_data))
        root = tree.iter('item')  #   Get the subtree with key as 'item'

        article_list = []
        for child in root:    #   Iterate to all nodes with key 'item'

            np_extractor = NPExtractor(child.find('description').text)
            result = np_extractor.extract()

            current_article_dict = {
                "title": child.find('title').text,
                "description": child.find('description').text,
                "articleUrl": child.find('link').text,
                "keywords": result
            }

            #print(current_article_dict.get('title'))

            article_list.append(current_article_dict)

        #print(article_list)

        first_article = article_list[0]
        #print(first_article)
        #getIrishTimesArticle(first_article.get('articleUrl'))

        return article_list

    except Exception as e:
        print(e)

def get_irish_times_article(dLink):

    artileHttp = urllib3.PoolManager()
    articleResponse = artileHttp.request('GET', dLink)
    articleRdata = articleResponse.data
    soup = BeautifulSoup(articleRdata)
    inputTag = soup.findAll(attrs={"class" : "no_name"})
    headline = soup.findAll(attrs={"property" : "headline"})[0].get_text()
    description = soup.findAll(attrs={"property" : "description"})[0].get_text()
    article = ""

    for node in inputTag:
        article+=(node.get_text())

    np_extractor = NPExtractor(article)
    result = np_extractor.extract()

    article_dict = {
                "title": headline,
                "description": description,
                "articleUrl": dLink,
                "articleContent": article,
                "keywords": result
            }

    #print("Headline: " + headline + "\n" + "Description: " + description + "\n\n" + "Article:\n" + article)
    #print("\n\nKeywords:\n" + "\n".join(result))

    return article_dict



# This is a fast and simple noun phrase extractor (based on NLTK)
# Feel free to use it, just keep a link back to this post
# http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
# http://www.sharejs.com/codes/
# Create by Shlomi Babluki
# May, 2013


# This is our fast Part of Speech tagger
#############################################################################

brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"
#############################################################################


class NPExtractor(object):

    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI":
            #if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches

print(get_article_list("lifestyle"))

#get_irish_times_article('http://www.irishtimes.com/news/world/europe/italian-police-seize-1-6-bn-of-assets-in-mafia-bust-1.2277807')