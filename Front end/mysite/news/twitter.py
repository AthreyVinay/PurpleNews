__author__ = 'Work'

import tweepy


def search(keywords):

    auth = tweepy.OAuthHandler('DFuMLbEuenPTnrCfiPUwVuNHG', '2p6jAKwsull7vfDQkfjgm1TMQRyf0u2ciIP6vvhaXAlQztoVJ3')
    auth.set_access_token('305656793-y7byCZEg8AaWB33U8s57khP5r6gFoiBuylNe5wR3', 'GD7OxNkz7kGzzRkE5dhV2KUnM2qbZCqABpU1w1BW2uFTG')
    api = tweepy.API(auth)

    tweets = api.search(keywords,'en', count = 10)

    return tweets