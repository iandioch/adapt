import sys

import xml.etree.ElementTree as ET

def get_file_content(name):
    name = name.strip()
    tree = ET.parse(name)
    root = tree.getroot()
    text = root[1][0]
    return '\n'.join(child.text for child in text if (child.attrib.get('crawlinfo') != 'boilerplate') and child.text is not None)

def collate_files(d):
    s = []
    with open(d, 'r') as f:
        for line in f:
            s.append(get_file_content(line))
    return '\n'.join(s)
    

if __name__ == '__main__':
    d = ' '.join(sys.argv[1:])
    collated = collate_files(d)
    output_file = d + '.collated.txt'
    with open(output_file, 'w') as f:
        f.write(collated)
        f.write('\n')
