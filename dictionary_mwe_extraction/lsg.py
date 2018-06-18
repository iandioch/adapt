import sys

def get_mwes_from_entry(p):
    s = p.split('\n')[0]
    if len(s) == 0 or s[0] != '#':
        return []
    t = s.strip('# ').split(',')
    return [u.strip() for u in t if len(u.split()) > 1]

def main():
    p = sys.stdin.read().split('\n\n')
    mwes = []
    for q in p:
        mwes.extend(get_mwes_from_entry(q))
    print('\n'.join(sorted(set(mwes))))

if __name__ == '__main__':
    main()
