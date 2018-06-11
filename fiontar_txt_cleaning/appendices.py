import sys

def split_ga_file(path):
    return []

def split_en_file(path):
    return []

def write_output(ga, en):
    if len(ga) != len(en):
        print('Must have same number of appendices.')
        return
    print('ga\ten')
    for a, b in zip(ga, en):
        print(a, b, sep='\t')

if __name__ == '__main__':
    ga_file = sys.argv[1]
    en_file = sys.argv[2]
    
    ga_appendices = split_ga_file(ga_file)
    en_appendices = split_en_file(en_file)
    write_output(ga_appendices, en_appendices)
