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
    for ch in e.findall('.//{urn:NEIDTRANS}ChunkCnt'):
        en = ch.find('{urn:NEIDTRANS}CHUNK')
        b = {'en': en.text, 'ga': []}
        for tr in ch.findall('.//{urn:NEIDTRANS}TR'):
            b['ga'].append(tr.text)
        d['ex'].append(b)
    return d

def get_collocations_from_entry(entry):
    hwd_obj = entry.find('.//{urn:NEIDTRANS}HWD')
    hwd = None
    a = {'hwd': None, 'entries': []}
    if hwd_obj is not None:
        a['hwd'] = hwd_obj.text.strip()

    blks = ['Adj', 'Adv', 'Conj', 'Det', 'Interj', 'Noun', 'Num', 'V_mod',
            'V_aux', 'Prep', 'Pron', 'Pref', 'Suff', 'Verb']
    for blk in blks:
        q = './/{urn:NEIDTRANS}' + blk + 'Blk/{urn:NEIDTRANS}FwkSenCnt'
        for pos in entry.findall(q):
            d = get_data_from_pos(pos)
            a['entries'].append(d)
    for pos in entry.findall('.//{urn:NEIDTRANS}PhrBlk/{urn:NEIDTRANS}PhrCnt/{urn:NEIDTRANS}FwkSenCnt'):
        d = get_data_from_pos(pos)
        a['entries'].append(d)
    for sub in entry.findall('.//{urn:NEIDTRANS}SUBBlk/{urn:NEIDTRANS}SubFormCnt'):
        # Eg. "abduct" entry.
        for pos in sub.findall('{urn:NEIDTRANS}FwkSenCnt'):
            d = get_data_from_pos(pos)
            form_obj = pos.find('.//{urn:NEIDTRANS}SUBFORM')
            form = None
            if form_obj is not None:
                form = form_obj.text
            d['subform'] = form
            a['entries'].append(d)
    for sen in entry.findall('./{urn:NEIDTRANS}DEnt/{urn:NEIDTRANS}FwkSenCnt'):
        # Eg. "accommodation office" entry.
        d = get_data_from_pos(sen)
        a['entries'].append(d)
    for phr in entry.findall('.//{urn:NEIDTRANS}FwkMWEBlk/{urn:NEIDTRANS}PhrVBlk/{urn:NEIDTRANS}PhrVCnt'):
        # Eg. "abound with".
        form_obj = phr.find('.//{urn:NEIDTRANS}PHRV')
        form = None
        if form_obj is not None:
            form = form_obj.text
        for tr in phr.findall('{urn:NEIDTRANS}FwkSenCnt'):
            d = get_data_from_pos(tr)
            d['subform'] = form
            a['entries'].append(d)
    for phr in entry.findall('.//{urn:NEIDTRANS}FwkMWEBlk/{urn:NEIDTRANS}PhrBlk/{urn:NEIDTRANS}PhrCnt'):
        # Eg. "abound with".
        form_obj = phr.find('.//{urn:NEIDTRANS}PHR')
        form = None
        if form_obj is not None:
            form = form_obj.text
        for tr in phr.findall('{urn:NEIDTRANS}FwkSenCnt'):
            d = get_data_from_pos(tr)
            d['subform'] = form
            a['entries'].append(d)
    return [a]

def get_mwes_from_entries(entries):
    for e in entries:
        for f in e['entries']:
            pos = f['pos']
            if pos is None:
                pos = 'UNK'
            en = e['hwd']
            if 'subform' in f and f['subform'] is not None:
                en = en + ' (' + f['subform'].strip() + ')'
            if en is None:
                en = 'UNK'
            for g in f['ga']:
                if g is None:
                    continue
                if len(g.split()) > 1:
                    yield (g, pos, en)
    

def main(xml_path):
    ET.register_namespace('', 'urn:NEDITRANS')
    ET.register_namespace('d', 'urn:NEIDTRANS')
    ET.register_namespace('md', 'urn:DPS2-metadata')
    e = ET.parse(xml_path).getroot()
    entries = []
    for entry in e.findall('{urn:NEIDTRANS}Entry'):
        entries.extend(get_collocations_from_entry(entry))
    print(json.dumps(entries, indent=4))

    irish_mwes = get_mwes_from_entries(entries)
    with open('mwes.txt', 'w') as f:
        for mwe in sorted(set(irish_mwes)):
            f.write('\t'.join(mwe))
            f.write('\n')

if __name__ == '__main__':
    path = ' '.join(sys.argv[1:])
    main(path)
