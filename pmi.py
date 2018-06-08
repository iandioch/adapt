import math
import sys

from collections import defaultdict

PRECOMPUTE_BIGRAMS = True

def load_word_counts(path_to_file):
    d = defaultdict(int)
    with open(path_to_file, 'r') as f:
        for line in f:
            words = line.lower().split()
            for word in words:
                d[word] += 1
            if PRECOMPUTE_BIGRAMS:
                for i in range(len(words)-1):
                    a = words[i] + ' ' + words[i+1]
                    d[a] += 1
    return d

def count_bigram_in_corpus(corpus_path, bigram):
    print('counting', bigram)
    with open(corpus_path, 'r') as f:
        return sum(line.lower().count(bigram) for line in f)

def pmi(a, b, bigram, wordcounts, total_words):
    top = bigram[1]*total_words
    bottom = a[1] * b[1]
    print('---')
    print('{} ({})', bigram[0], bigram[1])
    print('{} ({}), {} ({})'.format(a[0], a[1], b[0], b[1]))
    print(top, bottom)
    if top == 0 or bottom == 0:
        return float("-inf")
    return math.log(top/bottom, 2)
            

def main(corpus_path):
    wordcounts = load_word_counts(corpus_path)
    topn = sorted(wordcounts, key = lambda x:-wordcounts[x])
    print([(n, wordcounts[n]) for n in topn[:20]])
    total_words = sum(wordcounts.values())
    for line in sys.stdin:
        a, b = line.lower().split()
        bigram = a + ' ' + b
        a_freq = wordcounts[a]
        b_freq = wordcounts[b]
        bigram_freq = wordcounts[bigram]
        if not PRECOMPUTE_BIGRAMS:
            bigram_freq = count_bigram_in_corpus(corpus_path, bigram)
        print('{}\t: {}'.format(bigram, bigram_freq))
        p = pmi((a, a_freq), (b, b_freq), (bigram, bigram_freq), wordcounts, total_words)
        print(p)

if __name__ == '__main__':
    corpus_path = ' '.join(sys.argv[1:])
    main(corpus_path)
