import math
import sys

from collections import defaultdict

PRECOMPUTE_BIGRAMS = True
GET_TOP_BIGRAM_PMI = True

def load_word_counts(path_to_file):
    d = defaultdict(int)
    e = defaultdict(int)
    with open(path_to_file, 'r') as f:
        for line in f:
            words = line.lower().split()
            for word in words:
                d[word] += 1
            if PRECOMPUTE_BIGRAMS:
                for i in range(len(words)-1):
                    a = words[i] + ' ' + words[i+1]
                    e[a] += 1
    return d, e

def count_bigram_in_corpus(corpus_path, bigram):
    print('counting', bigram)
    with open(corpus_path, 'r') as f:
        return sum(line.lower().count(bigram) for line in f)

def pmi(a, b, bigram, wordcounts, total_words, print_result=True):
    top = bigram[1]*total_words
    bottom = a[1] * b[1]
    if print_result:
        print('---')
        print('{} ({})'.format(bigram[0], bigram[1]))
        print('{} ({}), {} ({})'.format(a[0], a[1], b[0], b[1]))
        print(top, bottom)
    if top == 0 or bottom == 0:
        ans = float("-inf")
    else:
        ans = math.log(top/bottom, 2)
    if print_result:
        print('PMI: {}'.format(ans))
    return ans
            

def main(corpus_path):
    wordcounts, bigramcounts = load_word_counts(corpus_path)
    topn = sorted(wordcounts, key = lambda x:-wordcounts[x])
    print('Most common words:')
    print([(n, wordcounts[n]) for n in topn[:20]])
    topm = sorted(bigramcounts, key = lambda x:-bigramcounts[x])
    print('---\nMost common bigrams:')
    print([(n, bigramcounts[n]) for n in topm[:20]])
    total_words = sum(wordcounts.values())

    if GET_TOP_BIGRAM_PMI:
        pmis = []
        for bigram in bigramcounts:
            a, b = bigram.split()
            a_freq, b_freq = wordcounts[a], wordcounts[b]
            p = pmi((a, a_freq), (b, b_freq), (bigram, bigramcounts[bigram]), wordcounts, total_words, print_result=False)
            pmis.append((p, bigram))
        pmis.sort(reverse=True)
        print('---\nBigrams with highest PMIs:')
        print(pmis[:20])
    print('Input bigrams to get PMI of, with 2 space-separated words per line:')
    for line in sys.stdin:
        a, b = line.lower().split()
        bigram = a + ' ' + b
        a_freq = wordcounts[a]
        b_freq = wordcounts[b]
        bigram_freq = bigramcounts[bigram]
        if not PRECOMPUTE_BIGRAMS:
            bigram_freq = count_bigram_in_corpus(corpus_path, bigram)
        p = pmi((a, a_freq), (b, b_freq), (bigram, bigram_freq), wordcounts, total_words)

if __name__ == '__main__':
    corpus_path = ' '.join(sys.argv[1:])
    main(corpus_path)
