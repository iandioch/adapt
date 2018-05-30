import sys

import xml.etree.ElementTree as ET

def convert_dix_file(name):
    name = name.strip()
    tree = ET.parse(name)
    root = tree.getroot()
    text = root[1][0]
    dic_section = root.find('section')
    out = []
    for pair in dic_section:
        p = pair.find('p')
        if p is None:
            continue
        l = p[0].text
        r = p[1].text
        if l is None or r is None:
            continue
        l = l.lower()
        r = r.lower()
        out.append('{} @ {}'.format(l, r))
    out.sort()
    return '\n'.join(out)

if __name__ == '__main__':
    d = ' '.join(sys.argv[1:])
    dic = convert_dix_file(d)
    output_file = d + '.dic'
    with open(output_file, 'w') as f:
        f.write(dic)
        f.write('\n')
