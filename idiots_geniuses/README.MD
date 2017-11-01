# Idiots & Geniuses: Twitter Data Collection.

### Aim

Collect counts of occurances of usernames in tweets associated with given terms over
an extended period of time.

### Usage

Make sure requirements are installed and you will also need to make sure you have access tokens, etc from twitter.
For more info on this: https://dev.twitter.com/streaming/overview or google it. Then you can just run it.

```bash
$ python collectCounts.py
```

Here the term being tracked are 'idiot' and 'genius'. If you want to change this
just update the varible `filterTerms` in the `if __name__ == __main__:` section to a
list/tuple or your choice.

### requirements
* tweepy==3.5.0
* python-dotenv==0.7.1