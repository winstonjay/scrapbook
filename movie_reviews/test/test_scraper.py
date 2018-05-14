import unittest
from bs4 import BeautifulSoup

import scraper


class TestChain(unittest.TestCase):

    def test_find_score(self):
        self.assertEqual(scraper.parse_score('<poodsclass="312"/>'), '312')
        self.assertEqual(scraper.parse_score('class="05"'), '05')
        self.assertEqual(scraper.parse_score('05'), '25')
        self.assertEqual(scraper.parse_score(test_row), '20')

    def test_find_review(self):
        self.assertEqual(scraper.parse_review(test_row),
            "this was actually a movie right. i am test_string.")


test_row = BeautifulSoup('''
<div class="row review_table_row">
    <div class="col-xs-8">
    </div>
    <div class="col-xs-16">
        <div class="user_review">
            <div class="scoreWrapper">
                <span class="20"></span>
            </div>
            this was actually a movie right. i am test_string.
        </div>
    </div>
</div>
''', 'html.parser').findAll('div', class_='row review_table_row')[0]

if __name__ == '__main__':
    unittest.main()