import urllib.request
from bs4 import BeautifulSoup
import re

import nltk
from nltk.corpus import brown

categories = ['news','opinion/','business','money','sport',
              'life','arts','puzzles']

urlb = 'http://www.thetimes.co.uk/tto'




class UKarticles:
    def getNewsByCategory(self,category):

        if category in categories:
            url = urlb.__add__('/' + category + '/')
            # print('url is %s',url)

            content = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(content, from_encoding='GB18030')


            articleTitle = []
            articleURL = []
            articleImage = []
            articleKeyword = []
            articleSummary = []
            articleDate = []

            if category == 'sport' or category == 'business' or category == 'money':
                hotNews = soup.find_all(class_=re.compile('article-'))
                print(hotNews)
                for i in hotNews:
                    # title
                    j = i.find('h2')
                    # print(j)
                    if j is not None:

                        articleTitle.append(j.text)
                        articleURL.append(j.a['href'])
                        print(j.text)
                        # print(j.a['href'])
                        urlbase = 'http://www.thetimes.co.uk'
                        url = urlbase.__add__(str(j.a['href']))

                        imageUrl = self.getimageFromURL(url)
                        articleImage.append(imageUrl)

                        # print (imageUrl)
                        # keyword in title
                        np_extractor = NPExtractor(j.text)
                        result = np_extractor.extract()
                        # print ('This article is about:',result)
                        articleKeyword.append(result)

                    # news contents
                    t = i.find('div', {'class', 'ellipsis'})
                    if t is not None:
                        # print(t.text)
                        articleSummary.append(t.text)


                    # news date
                    d = i.find('div', {'class', 'f-regular-update'})
                    if d is not None:
                        # print(d.text)
                        articleDate.append(d.text)

                article_dict = {'title':articleTitle,'url':articleURL,'imageUrl':articleImage,'keyword':articleKeyword,
                            'summary':articleSummary,'date':articleDate}


                return article_dict




    def getimageFromURL(url):
        # print(url)
        req  = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
             if hasattr( e, 'reason' ):
                 print( 'Fail in reaching the server -> ', e.reason )
                 return False
             elif hasattr( e, 'code' ):
                 print( 'The server couldn\'t fulfill the request -> ', e.code )
                 return False
             else:
                content1 = response.read()
                soup1 = BeautifulSoup(content1, from_encoding='GB18030')
                contents = soup1.find_all('div',{'class','tto-slideshow'})[0].find('img')
                result = contents['src']
                return result
        # print(contents)
        # if contents is not None:
        #     result = contents.ul.li.img['src']
        # # print(result)
        # return result









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


# Main method, just run "python np_extractor.py"
# def main():
#
#     sentence = "Swayy is a beautiful new dashboard for discovering and curating online content."
#     np_extractor = NPExtractor(sentence)
#     result = np_extractor.extract()
#     print ('This sentence is about:',result)
#
# if __name__ == '__main__':
#   main()



#
# doc = UKarticles.getNewsByCategory(UKarticles,'business')
#
#
# print(doc)