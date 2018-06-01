import csv
import sys

def is_too_long(line, normal_num_words=10):
    return len(line.split()) > normal_num_words

def is_numeral(s):
    ROMAN_NUMERALS = set('IVX')
    try:
        d = int(s.replace('£', ''))
        return d < 150
    except:
        return all(c in ROMAN_NUMERALS for c in s.strip())

def has_fullstops_in_middle(line):
    OK_WORDS = set(['no', 'uimh', 'cent'])
    s = line.split('.')
    c = 0
    for t in s:
        t = t.strip()
        if not len(t):
            continue
        words = t.split()
        if len(words) and (words[-1].lower() in OK_WORDS or is_numeral(words[-1])):
            continue
        c += 1
    return c > 1

def main(path):
    en_too_long = lambda s: is_too_long(s, normal_num_words=60)
    ga_too_long = lambda s: is_too_long(s, normal_num_words=64)

    writer = csv.writer(sys.stdout)
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            en, ga, score = row
            en_long = en_too_long(en)
            ga_long = ga_too_long(ga)

            weird_fullstops = has_fullstops_in_middle(en) or has_fullstops_in_middle(ga)
            too_long = en_long or ga_long
            writer.writerow((en, ga, score, too_long, weird_fullstops))


if __name__ == '__main__':
    main(' '.join(sys.argv[1:]))
