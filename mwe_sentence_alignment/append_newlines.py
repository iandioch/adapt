import sys

def main(f):
    OK_ENDS = set('.:!?,"')
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line[-1] not in OK_ENDS:
            line += '.'
        print(line + ' NEWLINE')

if __name__ == '__main__':
    main(sys.stdin)
