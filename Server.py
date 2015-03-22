from flask import Flask, render_template, request
from TweetParser import TweetParser
app = Flask(__name__)

app.debug = True
app.host = '0.0.0.0'

myparser = TweetParser('NetNeutrality')
target_names = ["Hostile", "Nice", "Happy", "Sad", "Angry"]

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        tagged_categories = request.form.getlist('category')
        tweet_id = int(request.form['tweetId'])
        cat = []
        for tag in tagged_categories:
            i = target_names.index(tag)
            if i != None:
                cat.append(i)
        myparser.add_tags(tweet_id, cat)

    tweet = myparser.getNextTweet()
    return render_template("root.html", tweet=tweet, categories=target_names)


@app.route("/train")
def train():
    myparser.train()
    return 'trained'

@app.route("/predict")
def predict():
    return str(myparser.test())

if __name__ == "__main__":
    app.run()
