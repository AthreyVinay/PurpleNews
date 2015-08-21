import urllib.request
from bs4 import BeautifulSoup
import re

import nltk
from nltk.corpus import brown

categories = ['news','opinion','business','money','sport',
              'lifestyle','arts','politics','culture']

urlb = 'http://www.telegraph.co.uk'


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

                        np_extractor = NPExtractor(title)
                        keywords = np_extractor.extract()

                        Url = j.a['href']
                        articleUrl = urlb.__add__(Url)
                        if articleUrl is not None:

                            # news image url
                            # t = i.find('div', {'class', 'piccentre'})
                            t = i.find(class_=re.compile('containerdiv'))
                            if t is not None:

                               # image url
                               #imageUrl  = t.img['src']

                               #  sumarry
                               su = i.find('div', {'class', 'labelAbstract'})
                               if su is not None:
                                 summary = su.a.text



                                 current_article_dict = {
                                    "title": title,
                                    "description": summary,
                                    "articleUrl": articleUrl,
                                    "imageUrl": imageUrl,
                                    "keywords":keywords
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

import nltk
from nltk.corpus import brown

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
