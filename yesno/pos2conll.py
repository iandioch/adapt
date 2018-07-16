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
    for line in inf:
        # Empty line = end of one sentence, start of the next.
        if len(line.strip()) <= 1:
            sents.append(curr_sent)
            curr_sent = []
            continue

        parts = line.strip().split()
        if len(parts) == 1:
            curr_word = parts[0]
            continue
        curr_sent.append((curr_word, *parts))
    curr_sent.append((curr_word, *parts))
    sents.append(curr_sent)
    print(sents)
    pass

if __name__ == '__main__':
    convert(sys.stdin, sys.stdout)
