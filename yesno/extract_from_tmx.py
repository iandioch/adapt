import re
import sys

import xml.etree.ElementTree as ET

YES_RE = re.compile('\\byes\\b')
NO_RE = re.compile('\\bno\\b')
NUMBER_RE = re.compile('no[.]*\s*[0-9]')

def is_yes_no_answer(en):
    en = en.lower()
    return YES_RE.search(en) or (NO_RE.search(en) and not NUMBER_RE.search(en))

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
            yield '\n'.join((prev_tu['en'], d['en'], '-', prev_tu['ga'], d['ga'], '---'))
        prev_tu = d

def parse_tmx(path):
    e = ET.parse(path).getroot()
    print('\n'.join(str(e) for e in find_question_answers(e)))

def main():
    xml_path = ' '.join(sys.argv[1:])
    parse_tmx(xml_path)
    pass

if __name__=='__main__':
    main()
