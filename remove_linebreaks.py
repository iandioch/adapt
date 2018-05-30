import sys

def get_all_input():
    return sys.stdin.readlines()

def remove_weird_newlines(inp):
    out = []
    curr = []
    for line in inp:
        line = line.strip()
        if len(line):
            curr.append(line)
        if len(line) and line[-1] == '.':
            cs = ' '.join(curr)
            out.append(cs)
            curr = []
    return '\n'.join(out)

if __name__ == '__main__':
    print(remove_weird_newlines(get_all_input()))
