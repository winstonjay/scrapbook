# -*- coding: utf-8 -*-
import unittest

from chain import read_tsv_file


class TestChain(unittest.TestCase):

    def test_read_tsv_file(self):
        test_data = "test/test_reviews.tsv"
        expect = ('<s>', '21213', '.', 'this', 'is', 'a', 'review', '?', '?',
                  '!', '!', ',', '.', '.', '</s>', '<s>', 'cats', ';', 'are',
                  'not', 'dogs', '.', '"', 'so', 'what', '"', '</s>', '<s>',
                  '!', 'hello', 'demos', '.', ',', '"', 'cool', '"',
                  '</s>')
        for got, want in zip(read_tsv_file(test_data), expect):
            self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()