import csv
import sys

'''
Takes an infile and outfile to read from and write to, respectively.
'''
def convert(inf, outf):
    writer = csv.writer(outf, dialect=csv.excel_tab)

    sents = []
    curr_sent = []
    curr_word = None

    # irishfst might output multiple guesses for a POS. This should be True if
    # this is the case, and the current line is a second or third guess for a given
    # token
    skip_pos = False
    for line in inf:
        # Empty line = end of one sentence, start of the next.
        if len(line.strip()) <= 1:
            sents.append(curr_sent)
            curr_sent = []
            continue
        should_add = True

        parts = line.strip().split()
        if len(parts) == 1:
            curr_word = parts[0]
            skip_pos = False
            continue
        if skip_pos:
            continue
        skip_pos = True
        curr_sent.append((curr_word, *parts))
        curr_word = None
    if curr_word is not None:
        curr_sent.append((curr_word, *parts))
    sents.append(curr_sent)

    for sent in sents:
        for index, word in enumerate(sent):
            print(word)
            surface_form, lemma, *details = word
            coarse_pos, *details = details
            if len(details):
                fine_pos, *morphology = details
            else:
                fine_pos = '_'
                morphology = []
            surface_form = surface_form.strip('"<>')
            lemma = lemma.strip('"')
            if len(morphology) == 0:
                morphology = '_'
            writer.writerow((index+1, surface_form, lemma, coarse_pos, fine_pos, '|'.join(morphology)) + ('_',)*4)

if __name__ == '__main__':
    convert(sys.stdin, sys.stdout)
