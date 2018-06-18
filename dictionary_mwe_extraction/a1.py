# xmlns="urn:NEIDTRANS" xmlns:d="urn:NEIDTRANS" xmlns:md="urn:DPS2-metadata"

import json
import sys

import xml.etree.ElementTree as ET


NAMESPACES = {
    '': 'urn:NEIDTRANS',
    'd': 'urn:NEIDTRANS',
    'md': 'urn:DPS2-metadata'
}

def get_data_from_pos(e):
    print(ET.dump(e))
    d = {'ex': [], 'ga': []}
    #d['pos'] = e.find('.//{urn:NEIDTRANS}POS').attrib['code']
    for ga in e.findall('.//{urn:NEIDTRANS}TrCnt/{urn:NEIDTRANS}TrGp/{urn:NEIDTRANS}TR'):
        d['ga'].append(ga.text)
    for ex in e.findall('.//{urn:NEIDTRANS}ExCnt'):
        en = ex.find('{urn:NEIDTRANS}EX')
        b = {'en': en.text, 'ga': []}
        for tr in ex.findall('.//{urn:NEIDTRANS}TR'):
            b['ga'].append(tr.text)
        d['ex'].append(b)
    return d

def get_collocations_from_entry(entry):
    #print(ET.dump(entry))
    hwd_obj = entry.find('.//{urn:NEIDTRANS}HWD')
    hwd = None
    a = {'hwd': None, 'pos': []}
    if hwd_obj is not None:
        a['hwd'] = hwd_obj.text.strip()
    for pos in entry.findall('.//{urn:NEIDTRANS}DetBlk'):
        d = get_data_from_pos(pos)
        continue

        p = {'pos': pos.attrib['code'], 'ex': [], 'ga': []}
        for ga in pos.findall('./{urn:NEIDTRANS}TR'):
            p['ga'].append(ga.text)
        for ex in entry.findall('.//{urn:NEIDTRANS}ExCnt'):
            en = ex.find('{urn:NEIDTRANS}EX')
            b = {'en': en.text, 'ga': []}
            for tr in ex.findall('.//{urn:NEIDTRANS}TR'):
                b['ga'].append(tr.text)
            p['ex'].append(b)
        a['pos'].append(p)
    for pos in entry.findall('.//{urn:NEIDTRANS}NounBlk'):
        d = get_data_from_pos(pos)
        a['pos'].append(d)
        continue


    return [a]

def main(xml_path):
    ET.register_namespace('', 'urn:NEDITRANS')
    ET.register_namespace('d', 'urn:NEIDTRANS')
    ET.register_namespace('md', 'urn:DPS2-metadata')
    e = ET.parse(xml_path).getroot()
    entries = []
    n = 0
    for entry in e.findall('{urn:NEIDTRANS}Entry'):
        entries.append(get_collocations_from_entry(entry))
        n += 1
        if n > 1000:
            break
    print('entries:')
    print('\n'.join(json.dumps(e) for e in entries))

if __name__ == '__main__':
    path = ' '.join(sys.argv[1:])
    main(path)
