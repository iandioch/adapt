import csv
import sys

def is_numeral(s):
    ROMAN_NUMERALS = set('IVX')
    try:
        d = int(s.replace('£', ''))
        return d < 150
    except:
        return all(c in ROMAN_NUMERALS for c in s.strip())


def check_start(en, ga):
    ROMAN_NUMERALS = set('IVX')
    def get_first_word(line):
        s = line.split()
        if len(s) == 0:
            return None
        s = ''.join(c for c in s[0] if c not in set(' .(),'))
        if all(c.upper() in ROMAN_NUMERALS for c in s):
            return s
        try:
            d = int(s.replace('£', ''))
            return d
        except:
            if len(s) == 1:
                return s
            return None

    a = get_first_word(en)
    b = get_first_word(ga)
    return a != b

def main(path):
    en_too_long = lambda s: is_too_long(s, normal_num_words=60)
    ga_too_long = lambda s: is_too_long(s, normal_num_words=64)

    writer = csv.writer(sys.stdout)
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            en, ga, score, too_long, weird_full_stops = row
            start_does_not_match = check_start(en, ga)
            writer.writerow((en, ga, score, too_long, weird_full_stops, start_does_not_match))


if __name__ == '__main__':
    main(' '.join(sys.argv[1:]))
