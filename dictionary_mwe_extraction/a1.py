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
    d = {'ex': [], 'ga': []}
    pos = e.find('.//{urn:NEIDTRANS}POS')
    if pos is None:
        d['pos'] = None
    else:
        d['pos'] = pos.attrib['code']
    for ga in e.findall('./{urn:NEIDTRANS}TrCnt/{urn:NEIDTRANS}TrGp'):
        g = ga.find('{urn:NEIDTRANS}TR').text
        d['ga'].append(g)
    for ga in e.findall('./{urn:NEIDTRANS}FwkStrCnt/{urn:NEIDTRANS}TrCnt/{urn:NEIDTRANS}TrGp'):
        g = ga.find('{urn:NEIDTRANS}TR').text
        d['ga'].append(g)
    for ex in e.findall('.//{urn:NEIDTRANS}ExCnt'):
        en = ex.find('{urn:NEIDTRANS}EX')
        b = {'en': en.text, 'ga': []}
        for tr in ex.findall('.//{urn:NEIDTRANS}TR'):
            b['ga'].append(tr.text)
        d['ex'].append(b)
    return d

def get_collocations_from_entry(entry):
    hwd_obj = entry.find('.//{urn:NEIDTRANS}HWD')
    hwd = None
    a = {'hwd': None, 'entries': []}
    if hwd_obj is not None:
        a['hwd'] = hwd_obj.text.strip()
    for pos in entry.findall('.//{urn:NEIDTRANS}DetBlk/{urn:NEIDTRANS}FwkSenCnt'):
        d = get_data_from_pos(pos)
        a['entries'].append(d)
    for pos in entry.findall('.//{urn:NEIDTRANS}NounBlk/{urn:NEIDTRANS}FwkSenCnt'):
        d = get_data_from_pos(pos)
        a['entries'].append(d)
    for pos in entry.findall('.//{urn:NEIDTRANS}AdjBlk/{urn:NEIDTRANS}FwkSenCnt'):
        d = get_data_from_pos(pos)
        a['entries'].append(d)
    for pos in entry.findall('.//{urn:NEIDTRANS}VerbBlk/{urn:NEIDTRANS}FwkSenCnt'):
        d = get_data_from_pos(pos)
        a['entries'].append(d)
    for pos in entry.findall('.//{urn:NEIDTRANS}InterjBlk/{urn:NEIDTRANS}FwkSenCnt'):
        d = get_data_from_pos(pos)
        a['entries'].append(d)
    for pos in entry.findall('.//{urn:NEIDTRANS}PhrBlk/{urn:NEIDTRANS}PhrCnt/{urn:NEIDTRANS}FwkSenCnt'):
        d = get_data_from_pos(pos)
        a['entries'].append(d)
    for sub in entry.findall('.//{urn:NEIDTRANS}SUBBlk/{urn:NEIDTRANS}SubFormCnt'):
        for pos in sub.findall('{urn:NEIDTRANS}FwkSenCnt'):
            d = get_data_from_pos(pos)
            form = pos.find('{urn:NEIDTRANS}SUBFORM').text
            d['subform'] = form
            a['entries'].append(d)

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
