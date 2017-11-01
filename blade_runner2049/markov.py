import random


class MarkovNgramModel(dict):
    """MarkovNgramModel([['word1 word2' ..., ('word_n' count)], ...], N=3):
    constructs a ngram table from input from which superficial sentwences
    can be constructed by..."""
    def __init__(self, ngram_freqs, N=3):
        for key, value in ngram_freqs:
            if key in self:
                self[key].append(value)
            else:
                self[key] = [value]
        self.K = N - 1
        self.starts = [s.split() for s in self.keys() if '<s>' in s]
        self.keys = [k for k in self]

    def generate_sequence(self, est_len=20):
        """Generate a sequence of words and punctuation to emulate a sentence
        whilst under the est_len and a sentence delimeter hasn't been reached."""
        seq = random.choice(self.starts)[:]
        while seq[-1] != '</s>' and not (est_len < 0 and seq[-1] in '.!?'):
            prev = concat(seq[-self.K:])
            seq += [self.next_word(prev)]
            est_len -= 1
        return self.post_format(seq)

    def next_word(self, prev):
        """return a weighted choice of word based on the previous n words,
        if previous n words does not exist in ngram table return any random word."""
        next_possible = self.get(prev, random.choice(self.keys))
        return weighted_choice(*zip(*next_possible))

    def post_format(self, sentence):
        """Format sentence spaces with respect to punctuation."""
        return ''.join([' ' + s if s not in ('.,!?') else s
                        for s in sentence if s not in ('</s>', '<s>')])[1:]


######### Helper functions.

concat = ' '.join

def load_counts(sourcefile):
    """Load txt file with format: word1 word2 ... wordn count
    return formated to: ['word1 word2' ..., ('word_n' 'count')]"""
    mapfmt = lambda a: (concat(a[:-2]), (a[-2], int(a[-1])))
    with open(sourcefile) as model:
        return (mapfmt(line.split()) for line in model.readlines())

def weighted_choice(choices, weights):
    "Return random choice from choices relative to given weights."
    rnd = random.uniform(0, sum(weights))
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return choices[i]
    raise ValueError('Negative values in input')


if __name__ == '__main__':
    ngram_freqs = load_counts("data/all3.txt")
    mark =  MarkovNgramModel(ngram_freqs)
    for x in range(20):
        print("\t* {}".format(mark.generate_sequence(10)))
