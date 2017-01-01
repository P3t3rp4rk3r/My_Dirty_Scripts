#!/usr/bin/python3
__author__ = "Santhosh Baswa"

import re

def main():
    fh = open('raven.txt')
    for line in fh:
        if re.search('(Len|Neverm)ore', line):
            print(line, end='')

if __name__ == "__main__": main()
