import csv
import re
import sys

def main(path):
    out = []
    # eg. '305 O. 74, r. 117'
    odd = re.compile('([0-9]+)\s+O[.]\s([0-9]+)[,]\sr[.]\s([0-9]+)\s')
    # eg. 'O. 74, r. 111 304'
    even = re.compile('O[.]\s([0-9]+)[,]\sr[.]\s([0-9]+)\s+([0-9]+)\s')
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            en = row[0]
            ga = row[1]
            score = row[2]

            odd_ans = odd.search(ga)
            if odd_ans is not None:
                a = int(odd_ans[1])
                if a % 2 == 1:
                    ga = ga.replace(odd_ans[0], '')
                    
            even_ans = even.search(ga)
            if even_ans is not None:
                a = int(even_ans[3])
                if a % 2 == 0:
                    ga = ga.replace(even_ans[0], '')

            out.append((en, ga, score))
    writer = csv.writer(sys.stdout)
    for o in out:
        writer.writerow(o)
            

if __name__ == '__main__':
    main(' '.join(sys.argv[1:]))
