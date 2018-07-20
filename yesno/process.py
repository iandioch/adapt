'''
Input one line at a time, each being a question in Irish.
'''

import atexit
import fcntl
import io
import os
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

IRISHFST_PROC = None


def run_irishfst(line):
    global IRISHFST_PROC
    if IRISHFST_PROC is None:
        print('Starting irishfst')
        command = ['sh', PATH_TO_IRISHFST_SCRIPT]
        IRISHFST_PROC = subprocess.Popen(command, bufsize=1, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, encoding='utf-8', shell=True)
        #fcntl.fcntl(IRISHFST_PROC.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

    IRISHFST_PROC.stdin.write(line + '\n')
    print('WROTE:', line)
    IRISHFST_PROC.stdin.flush()
    output = []
    print('bop')
    print(dir(IRISHFST_PROC.stdout))
    s = IRISHFST_PROC.stdout.readline()
    print('got')
    while True:
        if len(s):
            output.append(s)
            print("OUTPUT:", output)
        s = IRISHFST_PROC.stdout.readline()
    output = '\n'.join(output)
    error = None
    #output, error = IRISHFST_PROC.communicate(input=line)
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

def close_procs():
    print('CLOSE_PROCS')
    IRISHFST_PROC.stdin.close()
    IRISHFST_PROC.wait()
    print('Return code =', IRISHFST_PROC.returncode)
    pass

if __name__ == '__main__':
    atexit.register(close_procs)
    main()
