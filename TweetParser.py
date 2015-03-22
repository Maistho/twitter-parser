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
        if os.path.isfile(filepath):
            self.f = open(filepath, 'r')

    def getNextTweet(self):

        t = self.f.readline()

        if t != '':
            return json.loads(t)
        else:
            return None

    def train(self):
        trainArr = []
        y_train = []
        x_test = []
        tweet = self.getNextTweet()
        i = 0
        print('say "h" for hostile, and anything else for non-hostile')
        while tweet and i < 10:
            h = input(tweet['text'] + '\n')
            y_train.append([ 0 if h=='h' else 1])
            trainArr.append(tweet['text'])

            i+=1
            tweet = self.getNextTweet()

        i = 0
        tweet = self.getNextTweet()
        while i < 5 and tweet:
            x_test.append(tweet['text'])

            i+=1
            tweet = self.getNextTweet()


        x_train = np.array(trainArr)

        target_names = ['Hostile', 'Not hostile']

        self.model = {
                'target_names': target_names,
                'y': y_train,
                'x': x_train
                }

        classifier = Pipeline([
            ('vectorizer', CountVectorizer(ngram_range=(1,2))),
            ('tfidf', TfidfTransformer()),
            ('clf', OneVsRestClassifier(LinearSVC()))
            ])

        classifier.fit(x_train, y_train)
        predicted = classifier.predict(x_test)

        for tweet, prediction in zip(x_test, predicted):
            print('%s => %s' % (tweet, ', '.join(target_names[x] for x in prediction)))

if __name__ == '__main__':
    # Define some parameters
    hashtag = 'NetNeutrality'

    if(len(sys.argv) == 2):
        hashtag = sys.argv[1]

    t = TweetParser(hashtag)
    t.train()
