import csv
import sys


def split_file(path, sep):
    if sep[-1] != ' ':
        sep += ' '
    with open(path, 'r') as f:
        parts = f.read().split(sep)
        return [sep + part for part in parts if len(part) > 1]

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
        writer.writerow(pair)

if __name__ == '__main__':
    ga_file = sys.argv[1]
    en_file = sys.argv[2]
    
    ga_appendices = split_ga_file(ga_file)
    en_appendices = split_en_file(en_file)
    write_output(ga_appendices, en_appendices)
