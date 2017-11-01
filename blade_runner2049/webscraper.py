'''
webscraper.py

Collects Rotten Tomato audience reviews from pages 1 - 52
and saves results in path 'data/rawout.txt'.

Output Format is:
0-50 | Review text...
'''
from bs4 import BeautifulSoup
import requests
import re
import os.path

URL = 'https://www.rottentomatoes.com/m/blade_runner_2049/reviews/'


def get_page(index, outfile, url=URL):
    "return dictionary containing score, review, date for each item"
    # Make request for each page, user beautiful soup to parse
    # write the score and review sperated by '|'
    result = requests.get(URL, params=dict(page=index, type='user'))
    soup = BeautifulSoup(result.text, 'html.parser')
    for row in soup.findAll('div', class_='row review_table_row'):
        score = find_score(row)
        body = find_review(row)
        outfile.write("{} | {}\n".format(score, body))
    return "Collected page: %d" % index

def find_review(row):
    "Return date and review text."
    return ''.join(row.find('div', class_='user_review').stripped_strings)

def find_score(string):
    "Return extracted score from className."
    return next(iter(score_pattern.findall(str(string))), None)

# from brief look seems like they only use double quotes.
score_pattern = re.compile(r'class="([0-9]+)"')


if __name__ == '__main__':
    try:
        # we only need to do this once.
        assert not os.path.exists('data/rawout.txt')
        with open('data/rawout.txt', 'w') as outfile:
            for index in range(1, 52):
                try:
                    print(get_page(index, outfile, url=URL))
                except:
                    print("Error @ index %d", index)
        print("done.")
    except:
        print("File already exists!")

