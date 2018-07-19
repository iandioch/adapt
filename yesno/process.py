'''
Input one line at a time, each being a question in Irish.
'''

import io
import subprocess
import sys

import analyse
import pos2conll

# Path to script to tokenise and run POS tagger.
PATH_TO_IRISHFST_SCRIPT = './irishfst_run.sh'
OUTPUT_IRISHFST_ERRORS = False

MALTPARSER_JAR_PATH = '/home/noah/work/misc_tools/maltparser/maltparser-1.9.1/maltparser-1.9.1.jar'
MALTPARSER_CONFIG_PATH = '/home/noah/work/misc_tools/maltparser/maltparser-1.9.1/'
MALTPARSER_CONFIG_NAME = 'IrishTreebankYesNo'
OUTPUT_MALTPARSER_ERRORS = False


def run_irishfst(line):
    command = ['sh', PATH_TO_IRISHFST_SCRIPT]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, encoding='utf-8')
    output, error = proc.communicate(input=line)
    if error is not None and OUTPUT_IRISHFST_ERRORS:
        print('irishfst error:')
        print(error)
    return output


def irishfst_output_to_conll(sents):
    inf = io.StringIO(sents)
    with io.StringIO() as outf:
        pos2conll.convert(inf, outf)
        outf.seek(0)
        return outf.read()


def parse_dependencies(sents):
    command = ['java', '-jar', MALTPARSER_JAR_PATH,
               '-c', MALTPARSER_CONFIG_NAME, '-m', 'parse',
               '-v', 'off']
    proc = subprocess.Popen(command, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, encoding='utf-8', cwd=MALTPARSER_CONFIG_PATH)
    output, error = proc.communicate(input=sents)
    if error is not None and OUTPUT_MALTPARSER_ERRORS:
        print('maltparser error:')
        print(error)
    return output


def process(line):
    # tokenise line
    # run POS tagger on it
    # convert to conllu
    # extract useful parts
    pos_tagged = run_irishfst(line)
    conll = irishfst_output_to_conll(pos_tagged)
    deps = parse_dependencies(conll)
    analyse.analyse(deps)


def main():
    for line in sys.stdin:
        process(line)


if __name__ == '__main__':
    main()
