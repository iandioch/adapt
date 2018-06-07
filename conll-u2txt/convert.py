import sys

def convert(f):
    lines = f.readlines()
    out = []
    for line in lines:
        if (not len(line.strip())) or line[0] == '#':
            continue
        s = line.split('\t')
        t = s[1]
        if t == 'NEWLINE':
            print(' '.join(out))
            out = []
        else:
            out.append(t)
    print(' '.join(out))

if __name__ == '__main__':
    convert(sys.stdin)
