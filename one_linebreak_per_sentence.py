import sys

def is_num(s):
    try:
        int(s)
        return True
    except:
        return False

def is_valid_fullstop(s):
    if s.endswith('No') or s.endswith('no'):
        return True
    if s.endswith('I'):
        return True
    lastword = s.split(' ')[-1]
    if '£' in lastword:
        return True
    return False

def get_all_input():
    return sys.stdin.read()

def newlinify(inp):
    out = []
    lines = inp.split('.')
    curr = ''
    for line in lines:
        line = line.strip()
        if is_num(line) or is_valid_fullstop(line):
            curr += line
        else:
            if len(curr):
                out.append(curr + '. ' + line)
            else:
                out.append(line)
            curr = ''
    return '.\n'.join(out)

if __name__ == '__main__':
    print(newlinify(get_all_input()))
