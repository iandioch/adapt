import csv
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
            q_ends_with_question_mark = (prev_tu['en'][-1] == '?')
            ans_is_at_start = (d['en'].lower().strip().startswith('yes') or
                               d['en'].lower().strip().startswith('no'))
            yield {
                'en_q': prev_tu['en'],
                'en_a': d['en'],
                'ga_q': prev_tu['ga'],
                'ga_a': d['ga'],
                'q_ends_with_?': q_ends_with_question_mark,
                'ans_is_at_start': ans_is_at_start
            }
        prev_tu = d

def parse_tmx(path):
    e = ET.parse(path).getroot()
    with open('yesno.csv', 'w') as csvfile:
        fieldnames = ['en_q', 'en_a', 'ga_q', 'ga_a', 'q_ends_with_?', 'ans_is_at_start']
        w = csv.DictWriter(csvfile, fieldnames = fieldnames)
        w.writeheader()
        for d in find_question_answers(e):
            w.writerow(d)
    print('\n'.join(str(e) for e in find_question_answers(e)))

def main():
    xml_path = ' '.join(sys.argv[1:])
    parse_tmx(xml_path)
    pass

if __name__=='__main__':
    main()
