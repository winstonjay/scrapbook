'''
ngrams.py

Save to disk ngrms of a given length to a text file.
'''
import re
import sys
import os.path
from collections import Counter

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('spanish'))
    extra_stopwords = set(nltk_stopwords.words('english'))
except:
    print('Need to install python package nltk or create own list of stopwords.')
    stopwords = set()
    extra_stopwords = set()


def generate_counts(rows, N=1, write_file=False):
    "Read loaded words into counters and if needs be save to disk."
    # neg, pos, all counters.
    C0, C1, C = Counter(), Counter(), Counter()
    for score, sentence in rows:
        # remove puctuation and split into indivdual words.
        for ngram in emit_ngrams(sentence, N):
            # Split counts into 2 bins: positive negative.
            # To make the data less sparse put the middle point in both.
            if score <= 0.5: C0[ngram] += 1
            if score >= 0.5: C1[ngram] += 1
            # allways count in global.
            C[ngram] += 1
    if write_file or not os.path.exists('data/pos%d.txt' % N):
        with open('data/pos%d.txt' % N, 'w') as pos, \
             open('data/neg%d.txt' % N, 'w') as neg, \
             open('data/all%d.txt' % N, 'w') as alln:
            for (negkey, poskey, allkey) in zip(C0, C1, C):
                neg.write('{} {}\n'.format(negkey, C0[negkey]))
                pos.write('{} {}\n'.format(poskey, C1[poskey]))
                alln.write('{} {}\n'.format(allkey, C[allkey]))
        print("Wrote new counts to disk")
    return C0, C1, C


def read_file(filename):
    "Read, fmt score 0.0-1.0, strip EOL, return list of tuples."
    rows = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                score, body = f.readline().split(' | ')
            except:
                print("Error! skipped:", line)
            try:
                score = (int(score) * 2.0) / 100
            except:
                score = 0.5
            rows.append((score, body.strip()))
    return rows

################ Some basic helpers.

def emit_ngrams(string, N=3):
    tokens = (tokenize(string) if N <= 1 else
              ['<s>'] + tokenize(string) + ['</s>'])
    return (' '.join(tokens[i:i+N]) for i in range(len(tokens)-(N-1)))

def tokenize(string):
    "Return string split into lowercase words and punctuation."
    return [s.lower() for s in token_pattern.findall(string)
            if s.lower() not in stopwords and len(s) < 30]

# find words with hyphens and apostrophes in or the single
# items of punctuation '!', '?', '.', ','.
token_pattern = re.compile(r"([A-Za-z0-9\'\-]+|\.+|,|\!|\?)")


if __name__ == '__main__':
    try:
        _, datafile, N, *write_file = sys.argv
        N = int(N)
        write_file = (write_file != [] and write_file[0] == 'T')
        loaded_file = read_file(datafile)
        if N == 1:
            # be more strict on what we include if single selection.
            stopwords = stopwords | extra_stopwords | set('.,?!')

        print("##### Summary: ")
        for i, counts in enumerate(generate_counts(loaded_file, N, write_file)):
            print(('neg:', 'pos:', 'all:')[i])
            print("\tTotal: %d" % len(counts.values()))
            print("\tTop 10:", counts.most_common(10))
            print("---")
    except ValueError:
        print("Need Args expected=N (int), optional=write_to_disk (T/F)")