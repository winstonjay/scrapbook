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
import logging
import argparse
from time import ctime
from threading import Timer
from collections import Counter

from os import path, environ
from dotenv import load_dotenv

from tweepy.streaming import StreamListener
from tweepy.api import API
from tweepy import OAuthHandler, Stream


class TweetStreamer(StreamListener):
    """TweetStreamer(terms=[], interval=1800, dump_count=5):
    provide methods for counting user mentions in tweets tracked by a given set
    of keywords used on twitter. Number of json dictionaries generated per day can
    be found by the following: (86400 / intervaltime) * dump_count * len(terms)
    By default it will save 480 entries every 24 hours.
    Class extends and overides Tweepy StreamListener methods; Source:
    https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py"""

    def __init__(self, terms, interval=1800, dump_count=5, filename="data.json"):
        """Overide the StreamListener __init__; we need to set the self.api
        if we do this if not we dont need to import the API Class."""
        self.api   = API()
        self.terms = terms
        self.store = dict((t, Counter()) for t in self.terms)
        self.interval = interval
        self.dump_count = dump_count
        self.filename = filename
        self.totalCounts = 0
        logging.info("Starting new session.")
        logging.info("Terms=('{}'). Interval={} (secs). n={}. file='{}'".format(
                     "', '".join(self.terms), self.interval, self.dump_count, self.filename))
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
        logging.warning("Stream error: Status {}".format(status))
        if status.code == 420:
            logging.critical("Exiting application. Status {}".format(status))
            return False

    def _updateCounts(self, mentions, text):
        """self._updateCounts(list): Work out which term we
        found then add user counts."""
        for term in self.terms:
            if term in text:
                for user in mentions:
                    self.store[term][user['screen_name']] += 1

    def _dataDumps(self):
        """for a given interval dump the top n number of users mentioned
        for each term."""
        updateJson(self.filename, self.store, ctime(), self.dump_count)
        logging.info("Saved to file: {} tweets this epoch.".format(self.totalCounts))
        self._resetCounts()
        Timer(self.interval, self._dataDumps).start()

    def _resetCounts(self):
        self.totalCounts = 0
        self.store = dict((t, Counter()) for t in self.terms)


def updateJson(filename, data, timestamp, n):
    """updateJson(str, Counter, str, int): if file exists add
    new dict with current time, else create a newfile and add
    dict to this."""
    try:
        with open(filename) as f:
            feed = json.load(f)
        feed["times"].append(timestamp)
        for term, counts in data.items():
            feed[term].append(counts.most_common(n))
            feed["n_{}".format(term)].append(sum(counts.values()))
    except FileNotFoundError: # only execute this if file hasent been created.
        logging.info("Created new file: '{}'.".format(filename))
        feed = {"times": []}
        for term, counts in data.items():
            feed[term] = []
            feed["n_{}".format(term)] = []
    # Save either new dict or an updated old one.
    with open(filename,  mode='w') as f:
        json.dump(feed, f)


def construct_parser():
    # Set up argparse with start as a positional arg and end as optional.
    parser = argparse.ArgumentParser()
    f_help = "file to save json output of collected counts. default='data.json'"
    i_help = "Itervals between count collections. Default='1800' (secs)."
    l_help = "File to output logs to. default=sys.stdout"
    parser.add_argument("-f", "--filename", help=f_help, type=str)
    parser.add_argument("-i", "--interval", help=i_help, type=int)
    parser.add_argument("-l", "--logfile", help=l_help, type=str)
    return parser

if __name__ == '__main__':
    parser = construct_parser()
    args = parser.parse_args()
    outfile = args.filename or 'data.json'
    interval = args.interval or 1800
    logfile = args.logfile or 'stream.log'
    # init logger so we know what happens.
    logging.basicConfig(filename=logfile,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        level=logging.INFO)
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
    # Add terms when we initalise our TweetStreamer instance.
    # set interval to half an hour.
    tweetStreamer = TweetStreamer(
        terms=filterTerms, interval=interval, filename=outfile)
    stream = Stream(auth=auth, listener=tweetStreamer)
    stream.filter(track=tweetStreamer.terms, async=True, languages=["en"])


