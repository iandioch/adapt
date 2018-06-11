import csv
import itertools
import re
import sys

URU_MAPPING = {
    'a´': 'á',
    'e´': 'é',
    'i´': 'í',
    'ı´': 'í',
    'o´': 'ó',
    'u´': 'ú'
}

def split_file(path, sep):
    order_marker_regex = re.compile('O[.]\s[0-9]+[,]\sr[.]\s[0-9]+\s')
    if sep[-1] != ' ':
        sep += ' '
    with open(path, 'r') as f:
        s = f.read()
        for uru in URU_MAPPING:
            s = s.replace(uru, URU_MAPPING[uru]).replace(uru.upper(), URU_MAPPING[uru].upper())
        parts = s.split(sep)
        return [sep + order_marker_regex.sub('', part) for part in parts if len(part) > 1]

def split_ga_file(path):
    return split_file(path, 'FOSCRÍBHINN')

def split_en_file(path):
    return split_file(path, 'APPENDIX')

def write_output(ga, en):
    if len(ga) != len(en):
        print('Must have same number of appendices.')
        return
    writer = csv.writer(sys.stdout)
    writer.writerow(['ga', 'en'])
    for pair in zip(ga, en):
        a = pair[0].split('\n')
        b = pair[1].split('\n')
        for line in itertools.zip_longest(a, b, fillvalue=''):
            writer.writerow(line)
        #writer.writerow(pair)

if __name__ == '__main__':
    ga_file = sys.argv[1]
    en_file = sys.argv[2]
    
    ga_appendices = split_ga_file(ga_file)
    en_appendices = split_en_file(en_file)
    write_output(ga_appendices, en_appendices)
