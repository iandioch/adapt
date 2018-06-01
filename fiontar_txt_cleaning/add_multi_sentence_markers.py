import csv
import sys

def is_too_long(line, normal_num_words=10):
    return len(line.split()) > normal_num_words

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
            too_long = en_long or ga_long
            writer.writerow((en, ga, score, too_long))


if __name__ == '__main__':
    main(' '.join(sys.argv[1:]))
