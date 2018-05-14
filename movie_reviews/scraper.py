# -*- coding: utf-8 -*-
'''
scraper.py :
Collects Rotten Tomato audience reviews from multiple pages and saves results
in tsv format; tsv fieldnames: score, review.
'''
from __future__ import print_function

import argparse
import re

import requests

from bs4 import BeautifulSoup

URL = "https://www.rottentomatoes.com/m/{}/reviews/"


def collect_reviews(filename, url, max_pages=100):
    '''
    collect reviews for a given url looping through max 100 pages but stopping
    when a page does not have the classname 'user_review' within its html.
    url must be pre formed.
    '''
    with open(filename, 'w') as fp:
        fp.write("score\treview\n")
        print("requesting from:", url)
        for index in range(1, max_pages):
            try:
                parse_page(fp, get_page(url, index))
                print("collected page %d" % index)
            except requests.exceptions.HTTPError as e:
                print("Request Error!\n%s" % e)
                break
            except StopIteration:
                print("No more reviews...")
                break
    print("done.")

def parse_page(fp, page):
    "write to tsv file score, review for each item within a page"
    soup = BeautifulSoup(page, 'html.parser')
    for row in soup.findAll('div', class_='row review_table_row'):
        score = parse_score(row)
        body = parse_review(row)
        fp.write("{}\t{}\n".format(score, body))

def get_page(url, index):
    "return the raw html text from page index."
    r = requests.get(url, params=dict(page=index, type='user'))
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    if "user_review" not in r.text:
        raise StopIteration
    return r.text

def parse_review(row):
    "Return date and review text."
    return ''.join(row.find('div', class_='user_review').stripped_strings)

def parse_score(string):
    "Return extracted score from className. return mid if score not found"
    return next(iter(score_pattern.findall(str(string))), "25")

# from brief look seems like they only use double quotes.
score_pattern = re.compile(r'class="([0-9]+)"')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate psuedo-random chains of text.")
    parser.add_argument('movie',
        type=str,
        help='movie title with underscores. (may need url id from site)')
    parser.add_argument('-f', '--filename',
        type=str,
        help='name of file to write to',
        default="rawout.tsv")
    parser.add_argument('-n', '--max_pages',
        type=int,
        help='Max number of samples to collect',
        default=100)
    args = parser.parse_args()

    url = URL.format(args.movie)
    collect_reviews(args.filename, url, args.max_pages)

