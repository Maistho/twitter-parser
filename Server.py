from flask import Flask, render_template, request
from TweetParser import TweetParser
app = Flask(__name__)


app.debug = True
myparser = TweetParser('gamergate')

def precision(c, tweets):
    """Computes precision for class `c` on the specified test data."""

    tp = 0
    fp = 0
    for tweet in tweets:
        if c in tweet['predictions']:
            if c in tweet['tags']:
                tp+=1
            else:
                fp+=1

    if(tp+fp == 0):
        return float('nan')
    else:
        return tp/(tp+fp)

def recall(c, tweets):
    """Computes recall for class `c` on the specified test data."""

    tp = 0
    fn = 0
    for tweet in tweets:
        if c in tweet['tags']:

            if c in tweet['predictions']:
                tp+=1
            else:
                fn+=1

    return tp/(tp+fn)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        try:
            tagged_categories = request.form.getlist('category')
            tweet_id = int(request.form['tweetId'])
        except KeyError:
            tweet = myparser.getNextTweet()
            return render_template("tag.html", tweet=tweet, categories=myparser.target_names)

        cat = []
        for tag in tagged_categories:
            i = myparser.target_names.index(tag)
            if i != None:
                cat.append(i)
        myparser.add_tags(tweet_id, cat)

    tweet = myparser.getNextTweet()
    return render_template("tag.html", tweet=tweet, categories=myparser.target_names)


@app.route("/train")
def train():
    success = myparser.train()
    return render_template('trained.html', success=success)

@app.route("/predict")
def predict():
    tweet = myparser.getNextTweet()
    predicted = myparser.predict([tweet['text']])
    return render_template('predict.html', tweet = tweet, prediction = predicted, categories=myparser.target_names)

@app.route("/test")
def test():
    predicted, tweets = myparser.test()

    new_tweets = []
    for tweet, prediction in zip(tweets, predicted):
        tweet['predictions'] = prediction
        new_tweets.append(tweet)

    cats = []
    for c in range(0, len(myparser.target_names)):
        cats.append({
            'name': myparser.target_names[c],
            'recall': recall(c, new_tweets),
            'precision': precision(c, new_tweets)
            })
    tagging = []
    for tweet, prediction in zip(tweets, predicted):
        tagging.append('%s: %s => %s' % (tweet['text'], ', '.join(myparser.target_names[x] for x in tweet['tags']), ', '.join(myparser.target_names[x] for x in prediction)))

    return render_template('test.html', cats=cats, tagging=tagging)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
