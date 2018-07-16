'''
Expects as input one one line the Gaeilge question.
'''

import io
import subprocess
import sys

import pos2conll

# Path to script to tokenise and run POS tagger.
PATH_TO_IRISHFST_SCRIPT = './irishfst_run.sh'

def run_irishfst(line):
    command = ['sh', PATH_TO_IRISHFST_SCRIPT]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    output, error = proc.communicate(input=line)
    return output

def irishfst_output_to_conll(sents):
    inf = io.StringIO(sents)
    outf = sys.stdout
    pos2conll.convert(inf, outf)

def process(line):
    # tokenise line
    # run POS tagger on it
    # convert to conllu
    # extract useful parts
    pos_tagged = run_irishfst(line)
    conll = irishfst_output_to_conll(pos_tagged)

def main():
    for line in sys.stdin:
               process(line)

if __name__ == '__main__':
    main()
