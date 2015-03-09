# twitter-parser

## How to run
Create and activate a virtual python environment:
```
virtualenv --python=python3 venv
. venv/bin/activate
```
Install the requirements:
```
pip install -r requirements.txt
```

Run the tweetfetcher
```
python3 TweetFetcher.py
```

##Authentication
Copy credentials to myCredentials.py
Then find your own credentials at apps.twitter.com and enter them into myCredentials.py


#Documentation
- [Pipeline](http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
- [CounterVectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)
- [Tfid Transformer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html#sklearn.feature_extraction.text.TfidfTransformer)
- [OneVsRestClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.multiclass.OneVsRestClassifier.html)
