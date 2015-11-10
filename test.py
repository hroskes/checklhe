import sys
import collections
import event

def checkflavors(file):
    with open(file) as f:
        for line in f:
            print line
            continue

if __name__ == '__main__':
    checkflavors(sys.argv[1])
