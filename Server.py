from flask import Flask, render_template, request
from TweetParser import TweetParser
app = Flask(__name__)

app.host = '0.0.0.0'

myparser = TweetParser('NetNeutrality')

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

if __name__ == "__main__":
    app.run()
