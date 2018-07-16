'''
Expects as input one one line the Gaeilge question.
'''

import subprocess
import sys

# Path to script to tokenise and run POS tagger.
PATH_TO_IRISHFST_SCRIPT = './irishfst_run.sh'

def run_irishfst(line):
    command = ['sh', PATH_TO_IRISHFST_SCRIPT]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    output, error = proc.communicate(input=line)
    print(output)
    print(error)

def process(line):
    # tokenise line
    # run POS tagger on it
    # convert to conllu
    # extract useful parts
    pos_tagged = run_irishfst(line)

def main():
    for line in sys.stdin:
               process(line)

if __name__ == '__main__':
    main()
