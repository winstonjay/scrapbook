# -*- coding: utf-8 -*-
'''
chain.py
Generate psuedo-random chains of text.
usage: chain.py [-h] [-l LEN] [-n NUMBER] [-k SAMPLES] [-s SEED] [-f FILE]
Reference: https://golang.org/doc/codewalk/markov/
'''
from __future__ import print_function
from io import open # python 2/3

import re
import csv
import random
import argparse
from collections import defaultdict


def main():
    args = parse_args()
    c = Chain(args.prefix_len)
    c.build(read_tsv_file(args.file))
    for _ in range(args.samples):
        chain = c.generate(args.text_len, seed=args.seed)
        print(detokenize_text(chain))


class Chain(object):
    '''
    Chain contains a dict ("chain") of prefixes to a list of suffixes.
    A prefix is a string of prefixLen words joined with spaces.
    A suffix is a single word. A prefix can have multiple suffixes.
    '''
    def __init__(self, n=3):
        self.n = n
        self.chain = defaultdict(list)

    def build(self, iterable):
        '''
        Build reads text from the provided file_reader and parses it into
        prefixes and suffixes that are stored in Chain. A file reader is a
        iterator that emits tokens to be stored in the chain.
        '''
        prefix = [""] * self.n
        for s in iterable:
            self.chain[cat(prefix)].append(s)
            prefix = prefix[1:] + [s]

    def generate(self, text_len, seed=None):
        "generate returns a string of at most n words generated from Chain."
        if seed is not None:
            seed = seed.lower()
        else:
            seed = random.choice(list(self.chain))
        seed   = seed.split()
        prefix = seed[-self.n:]
        assert len(prefix) >= self.n, "Seed too short %d >=%d" % (len(prefix), self.n)
        return self._generate(text_len, seed, prefix)

    def _generate(self, text_len, words, prefix):
        "_generate executes the chain generation with properly prepared args"
        i, s = 0, str
        while i < text_len or s not in delimeters:
            choices = self.chain[cat(prefix)]
            if not choices:
                break
            s = random.choice(choices)
            words.append(s)
            prefix = prefix[1:] + [s]
            i += 1
        return words


def detokenize_text(tokens):
    '''
    Detokenizing a sentence converts an array of tokens back into a joined
    string, removing any id_tokens such as '<s>' and applying additonal
    formatting.
    '''
    # TODO: handle 'the "quoted items"'. current e.g.='text here is not" cool"'
    sentence = []
    tokens = iter(tokens)
    t = next(tokens, None)
    while t is not None:
        if t in id_tokens:
            t = next(tokens, None)
            continue
        if not sentence or t in punctuation:
            sentence.append(t)
        else:
            sentence.extend([" ", t])
        t = next(tokens, None)
    return "".join(sentence)


#### Helper functions

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate pseudo-random chains of text "
                    "from tsv file scraped with `scraper.py`.")
    parser.add_argument('file',
        type=str,
        help='Input file.')
    parser.add_argument('-n', '--text_len',
        type=int,
        help='estimate number of tokens to generate in each sample',
        default=10)
    parser.add_argument('-p', '--prefix_len',
        type=int,
        help='chain prefix length in tokens',
        default=3)
    parser.add_argument('-k', '--samples',
        type=int,
        help='number of samples to generate',
        default=1)
    parser.add_argument('-s', '--seed',
        type=str,
        help='start seed for text. length must be >= num')
    return parser.parse_args()

def read_tsv_file(filename):
    "emit file line by line"
    with open(filename, encoding="utf-8") as fp:
        reader = csv.DictReader(fp, delimiter='\t')
        for row in reader:
            yield start
            for word in tokenizer.findall(row['review'].lower()):
                yield word
            yield end


tokenizer   = re.compile(r"[\w'a-zA-ZÀ-ÖØ-öø-ÿ]+|[.,!?\";]")
punctuation = set(".,!?;")
start       = "<s>"
end         = "</s>"
id_tokens   = set([start, end])
delimeters  = set(".?.!") | id_tokens

cat = " ".join

# not in use but saving for another time
# conjunctions = set('''
# although and as because but either we even even even how however
# they if in in neither or otherwise since unless what when whether
# despite that
# '''.split())


if __name__ == '__main__':
    main()