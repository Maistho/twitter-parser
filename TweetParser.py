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
        self.hashtag = hashtag
        try:
            with open('.linenum', 'r') as f:
                lines = int(f.readline())
        except:
            lines = 0
        filepath = 'tweets/' + hashtag + '.json'
        self.f = open(filepath, 'r')
        self.f.seek(lines)
        self.target_names = ["Hostile", "Nice", "Happy", "Sad", "Angry"]
        self.tweets = {}
        self.classifier = None

    def getNextTweet(self):

        t = self.f.readline()

        if t != '':
            tweet = json.loads(t)
            self.tweets[tweet['id']] = tweet
            with open('.linenum', 'w') as f:
                f.write(str(self.f.tell()))
            return tweet
        else:
            return None

    def add_tags(self, id, tags):
        if type(tags) is list:
            self.tweets[id]['tags'] = tags
            with open('tags/' + self.hashtag + '.json', 'a') as f:
                f.write(json.dumps(self.tweets[id]) + '\n')
            return True
        else:
            return False

    def get_tagged_tweets(self):

        with open('tags/' + self.hashtag + '.json', 'r') as f:

            tweets = []
            t = f.readline()
            while t != '':
                tweet = json.loads(t)
                tweets.append(tweet)
                t = f.readline()
        if len(tweets) > 0:
            return tweets
        else:
            return None

    def predict(self, tweets):
        if self.classifier != None:
            predicted = self.classifier.predict(tweets)
            return predicted
        else:
            return None

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
            for tweet in self.get_tagged_tweets():
                if 'tags' in tweet.keys():
                    trainArr.append(tweet['text'])
                    y_train.append(tweet['tags'])
            if len(y_train) == 0 or len(trainArr) == 0 or len([item for sublist in y_train for item in sublist]) == 0:
                return False

        x_train = np.array(trainArr)

        classifier = Pipeline([
            ('vectorizer', CountVectorizer(ngram_range=(1,2))),
            ('tfidf', TfidfTransformer()),
            ('clf', OneVsRestClassifier(LinearSVC()))
            ])

        classifier.fit(x_train, y_train)
        self.classifier = classifier
        return True

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

        predicted = self.predict(x_test)

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
