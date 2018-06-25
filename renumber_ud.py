import sys

def end_of_sentence(lines):
    if len(lines) == 0:
        return
    for i, line in enumerate(lines):
        p = line.strip().split('\t')
        print('\t'.join([str(i+1)] + p[1:]))

def main():
    lines = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if line[0] == '#':
            print(line)
        elif len(line) < 2:
            end_of_sentence(lines)
            lines = []
        else:
            lines.append(line)
    end_of_sentence(lines)

if __name__ == '__main__':
    main()
