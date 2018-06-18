# xmlns="urn:NEIDTRANS" xmlns:d="urn:NEIDTRANS" xmlns:md="urn:DPS2-metadata"

import sys

import xml.etree.ElementTree as ET


NAMESPACES = {
    '': 'urn:NEIDTRANS',
    'd': 'urn:NEIDTRANS',
    'md': 'urn:DPS2-metadata'
}

def get_collocations_from_entry(entry):
    #print(ET.dump(entry))
    hwd_obj = entry.find('.//{urn:NEIDTRANS}HWD')
    hwd = None
    if hwd_obj is not None:
        hwd = hwd_obj.text.strip()
    return [hwd]

def main(xml_path):
    ET.register_namespace('', 'urn:NEDITRANS')
    ET.register_namespace('d', 'urn:NEIDTRANS')
    ET.register_namespace('md', 'urn:DPS2-metadata')
    e = ET.parse(xml_path).getroot()
    collocations = []
    n = 0
    for entry in e.findall('{urn:NEIDTRANS}Entry'):
        collocations.extend(get_collocations_from_entry(entry))
        n += 1
        if n > 1000:
            break
    print('collocations:')
    print('\n'.join(collocations))

if __name__ == '__main__':
    path = ' '.join(sys.argv[1:])
    main(path)
