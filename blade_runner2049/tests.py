from ngrams import *
from webscraper import *

def preprocess_tests():
    teststr1 = "Really happy... I finally was able to see this! Highly recommend."
    teststr2 = "..sad..!don't tell me 'tis a good film"
    teststr3 = "THIS_WAS_AWESOME!!!"
    assert tokenize("99 1hundred, ok!") == ['99', '1hundred', ',', 'ok', '!']
    assert tokenize(teststr1) == ['really', 'happy', '.', '.', '.', 'i',
                                        'finally', 'was', 'able', 'to', 'see',
                                        'this', '!', 'highly', 'recommend', '.']
    assert tokenize(teststr2) == ['.', '.', 'sad', '.', '.', '!', "don't",
                                        'tell', 'me', "'tis", 'a', 'good', 'film']
    assert tokenize(teststr3) == ['this', 'was', 'awesome', '!', '!', '!']


def webscraper_tests():
    assert find_score('<poodsclass="312"/>') == '312'
    assert find_score('class="05"') == '05'
    assert find_score('05') == None
    print('All tests pass.')


if __name__ == '__main__':
    preprocess_tests()
    webscraper_tests()