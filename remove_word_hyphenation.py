import re
import sys

def main():
    t = re.compile('\s[a-z]+([-]\s)[a-z]+\s')
    t = re.compile('\s\w+([-]\s)[^\s]+\s')
    for line in sys.stdin.readlines():
        a = t.search(line)
        if a is not None:
            line = line.replace(a[1], '')
        print(line.strip())
    
    

if __name__ == '__main__':
    main()
