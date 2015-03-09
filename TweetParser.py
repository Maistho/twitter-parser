import sys
import json
import os.path
from pprint import pprint

class TweetParser:

    def __init__(self, hashtag):
        filepath = 'tweets/' + hashtag + '.json'
        if os.path.isfile(filepath):
            self.f = open(filepath, 'r')

    def getNextTweet(self):

        t = self.f.readline()

        if t != '':
            return json.loads(t)
        else:
            return None

    def parse(self):
        tweet = self.getNextTweet()
        while tweet:
            # Do something with this tweet
            pprint(tweet['text'])
            tweet = self.getNextTweet()


if __name__ == '__main__':
    # Define some parameters
    hashtag = 'NetNeutrality'

    if(len(sys.argv) == 2):
        hashtag = sys.argv[1]

    t = TweetParser(hashtag)
    t.parse()
