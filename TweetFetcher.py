from multiprocessing import Process, JoinableQueue, Pool
from TwitterSearch import *
import json
import os.path
import signal
import sys
import myCredentials as credentials

q = JoinableQueue()

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def jsonWriter():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    while True:
        data = q.get()
        with open('tweets.json', 'a') as f:
            f.write(data + '\n')
        q.task_done()

def mkJson(tweet):
    q.put(json.dumps(tweet))


if __name__ == '__main__':


    # Define some parameters
    query = ['test']
    lang = 'en'
    include_entities = False

    #This process is responsible for writing to the file
    writer = Process(target=jsonWriter, )
    writer.start()
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(query)
        tso.set_language(lang)
        tso.set_include_entities(include_entities)

        ts = TwitterSearch(
                consumer_key = credentials.consumer_key,
                consumer_secret = credentials.consumer_secret,
                access_token = credentials.access_token,
                access_token_secret = credentials.access_token_secret,
                )

        with Pool(4,init_worker) as pool:
            for tweet in ts.search_tweets_iterable(tso):
                pool.apply_async(mkJson, (tweet,))


    except TwitterSearchException as e:
        print(e)

    except KeyboardInterrupt as e:
        print("\nClosing...")

    finally:
        q.join()
        writer.terminate()
        sys.exit(0)



