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
    keywords = []

    for i in url_list:
        url = i


    # url = 'http://deportes.elpais.com/deportes/2015/07/21/actualidad/1437504468_097396.html'
        a = Article(url,language = 'es')

        a.download()
        a.parse()

        title = translateToEn(a.title)
        imageUrl = a.top_image
        summary = translateToEn(a.text[:1500])

        np_extractor = NPExtractor(title)
        keywords = np_extractor.extract()

        current_article_dict = {
                                    "title": title,
                                    "description": summary,
                                    "articleUrl": url,
                                    "imageUrl": imageUrl,
                                    "keywords": keywords
                                  }
        spainArticles.append(current_article_dict)



    return spainArticles


def translateToEn(text):

    gs = goslate.Goslate()
    result = gs.translate(text,'en')
    return result


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


# print (getSpainArticlese(getSpainNews('business')))