import sys

def end_of_sentence(lines, outputted_id, curr_id):
    if len(lines) == 0:
        return
    if not outputted_id:
        print('# sent_id = {}'.format(curr_id))
    for i, line in enumerate(lines):
        p = line.strip().split('\t')
        print('\t'.join([str(i+1)] + p[1:]))
    print()

def main():
    lines = []
    outputted_id = False
    curr_id = 1
    for line in sys.stdin.readlines():
        line = line.strip()
        if len(line) < 2:
            end_of_sentence(lines, outputted_id, curr_id)
            lines = []

            outputted_id = False
            curr_id += 1
        elif line[0] == '#':
            if 'sent_id' in line:
                outputted_id = True
            print(line)
        else:
            lines.append(line)
    end_of_sentence(lines)

if __name__ == '__main__':
    main()
