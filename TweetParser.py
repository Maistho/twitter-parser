import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
import sys
import json
import os.path
from pprint import pprint

class TweetParser:

    def __init__(self, hashtag):
        filepath = 'tweets/' + hashtag + '.json'
        self.f = open(filepath, 'r')
        self.target_names = ["Hostile", "Nice", "Happy", "Sad", "Angry"]
        self.tweets = {}
        self.classifier = None

    def getNextTweet(self):

        t = self.f.readline()

        if t != '':
            tweet = json.loads(t)
            self.tweets[tweet['id']] = tweet
            return tweet
        else:
            return None

    def add_tags(self, id, tags):
        self.tweets[id]['tags'] = tags

    def classify_tweets(self, tweets):
        predicted = self.classifier.predict(tweets)
        return predicted

    def __get_categories(self):
        categories = []
        for i, cat in enumerate(self.target_names):
            print(str(i) + ': ' + cat)
        user_input = input()
        for cat in user_input.split():
            if int(cat) >= 0 and int(cat) < len(self.target_names):
                categories.append(int(cat))
        return categories


    def train(self, tag_tweets=False):
        trainArr = []
        y_train = []
        if tag_tweets:
            tweet = self.getNextTweet()

            print('Enter the numbers, separated by space, corresponding to the' +
                    'categories you think that the tweet belongs to.\n')

            #User Feedback-loop
            i = 0
            while tweet and i < 10:
                print(tweet['text'] + '\n')
                y_train.append(self.__get_categories())
                trainArr.append(tweet['text'])

                i+=1
                tweet = self.getNextTweet()
        else:
            for tweet in self.tweets.values():
                if 'tags' in tweet.keys():
                    trainArr.append(tweet['text'])
                    y_train.append(tweet['tags'])


        x_train = np.array(trainArr)

        classifier = Pipeline([
            ('vectorizer', CountVectorizer(ngram_range=(1,2))),
            ('tfidf', TfidfTransformer()),
            ('clf', OneVsRestClassifier(LinearSVC()))
            ])

        classifier.fit(x_train, y_train)
        self.classifier = classifier

    def test(self):
        if self.classifier != None:
            return False

        x_test = []
        i = 0
        tweet = self.getNextTweet()
        while i < 5 and tweet:
            x_test.append(tweet['text'])

            i+=1
            tweet = self.getNextTweet()

        predicted = self.classify_tweets(x_test)

        for tweet, prediction in zip(x_test, predicted):
            print('%s => %s' % (tweet, ', '.join(self.target_names[x] for x in prediction)))
        return predicted

if __name__ == '__main__':
    # Define some parameters
    hashtag = 'NetNeutrality'

    if(len(sys.argv) == 2):
        hashtag = sys.argv[1]

    t = TweetParser(hashtag)
    t.train(tag_tweets=True)
    t.test()
