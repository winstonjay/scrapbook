"""
collect_tweets.py

Aim:
    Collect counts of occurances of usernames in tweets associated with given terms over
    an extended period of time. Save summaries at repeated intervals to json file.
TODO:
    * consider futher TweetStreamer.on_error method.
    * If possible work out why break-downs occur after 3 days or so.


"""
from __future__ import print_function

import json
from time import ctime, sleep
from threading import Timer
from collections import Counter

from os import path
from os import environ
from dotenv import load_dotenv

from tweepy.streaming import StreamListener
from tweepy.api import API
from tweepy import OAuthHandler
from tweepy import Stream


class TweetStreamer(StreamListener):
    """TweetStreamer(terms=[], interval=1800, dumpCount=5):
    provide methods for counting user mentions in tweets tracked by a given set
    of keywords used on twitter. Number of json dictionaries generated per day can
    be found by the following:
        (86400 / intervaltime) * dumpCount * len(terms)
    By default it will save 480 entries every 24 hours.
    Class extends and overides Tweepy StreamListener methods; Source:
    https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py"""

    def __init__(self, terms, interval=1800, dumpCount=5, file="data.json"):
        """Overide the StreamListener __init__; we need to set the self.api
        if we do this if not we dont need to import the API Class."""
        self.api   = API()
        self.terms = terms
        self.store = dict((t, Counter()) for t in self.terms)
        self.interval = interval
        self.dumpCount = dumpCount
        self.file = file
        self.totalCounts = 0
        printLog("New session:")
        print("\tTerms=['{}']. Interval={}. secs. n={}. file='{}'".format(
            "', '".join(self.terms), self.interval, self.dumpCount, self.file))
        print("."*40)
        self._dataDumps() # init data saving thread.

    def on_status(self, status):
        """Acts when a status from twitter is recived. Take status
        and if applicable add counts to database"""
        if (not status.retweeted) and ('RT @' not in status.text):
            mentions = status.entities['user_mentions']
            self.totalCounts += 1
            if mentions:
                self._updateCounts(mentions, status.text)
        return True

    def on_error(self, status):
        printLog(status)
        if status.code == 420:
            return False

    def _updateCounts(self, mentions, text):
        """self._updateCounts(list): Work out which term we
        found then add user counts."""
        for term in self.terms:
            if term in text:
                for user in mentions:
                    self.store[term][user['screen_name']] += 1

    def _dataDumps(self, file="data.json"):
        """for a given interval dump the top n number of users mentioned
        for each term."""
        updateJson(self.file, self.store, ctime(), self.dumpCount)
        printLog("Saved to file: {} tweets this epoch.".format(self.totalCounts))
        self._resetCounts()
        print("...")
        printLog("Gathering Tweets..")
        Timer(self.interval, self._dataDumps).start()

    def _resetCounts(self):
        self.totalCounts = 0
        self.store = dict((t, Counter()) for t in self.terms)


def updateJson(filename, data, timestamp, n):
    """updateJson(str, Counter, str, int): if file exists add
    new dict with current time, else create a newfile and add
    dict to this."""
    try:
        with open('data.json') as f:
            feed = json.load(f)
        feed["times"].append(timestamp)
        for term, counts in data.items():
            feed[term].append(counts.most_common(n))
            feed["n_{}".format(term)].append(sum(counts.values()))
    except FileNotFoundError: # only execute this if file hasent been created.
        printLog("Created new file: '{}'.".format(filename))
        feed = {"times": []}
        for term, counts in data.items():
            feed[term] = []
            feed["n_{}".format(term)] = []
    # Save either new dict or an updated old one.
    with open('data.json',  mode='w') as f:
        json.dump(feed, f)


def printLog(*args, **kwargs):
    "std print function prefixed with timestamp."
    print(ctime()+":", *args, **kwargs)


if __name__ == '__main__':

    # update this to use your own terms.
    filterTerms = ("idiot", "genius")

    # Load dot-env file where auth tokens are stored.
    load_dotenv(path.join(path.dirname(__file__), '.env'))

    # Get and set env varibles to local varibles.
    access_token        = environ.get("Access_Token")
    access_token_secret = environ.get("Access_Token_Secret")
    consumer_key        = environ.get("Consumer_Key")
    consumer_secret     = environ.get("Consumer_Secret")

    # Set authentication tokens.
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    printLog("Starting Stream...")
    # Add terms when we initalise our TweetStreamer instance.
    # set interval to half an hour.
    tweetStreamer = TweetStreamer(terms=filterTerms,
                                  interval=1800)
    stream = Stream(auth=auth, listener=tweetStreamer)
    stream.filter(track=tweetStreamer.terms, async=True, languages=["en"])


