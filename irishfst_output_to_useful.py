import sys

def main():
    token = None
    for line in sys.stdin.readlines():
        c = line.strip().split()
        if len(c) == 0:
            continue
        elif len(c) == 1:
            # Original token
            token = c[0].strip('<>"')
            if len(token) == 0:
                token = None
            continue
        elif token is None:
            # Alternate POS, skip
            continue
        else:
            lemma, *tags = c
            lemma = lemma.strip('"')
            if tags[0] == 'Verbal':
                tags = [tags[0] + tags[1], *tags[2:]]
            print(lemma, tags[0], sep='|', end=' ')
            token = None

            if lemma == '.':
                print()

if __name__ == '__main__':
    main()
