import sys

import xml.etree.ElementTree as ET

def is_yes_no_answer(en):
    en = en.lower()
    return 'yes' in en or 'no' in en

def find_question_answers(e):
    prev_tu = None
    for tu in e.find('body'):
        d = {}
        for tuv in tu.iter('tuv'):
            lang = tuv.attrib['{http://www.w3.org/XML/1998/namespace}lang']
            lang = lang.split('-')[0]

            text = ''.join(tuv.itertext())
            text = text.strip()

            d[lang] = text
        if is_yes_no_answer(d['en']):
            yield (d['en'] + ' ' + d['ga'])
        prev_tu = tu

def parse_tmx(path):
    e = ET.parse(path).getroot()
    print('\n'.join(str(e) for e in find_question_answers(e)))

def main():
    xml_path = ' '.join(sys.argv[1:])
    parse_tmx(xml_path)
    pass

if __name__=='__main__':
    main()
