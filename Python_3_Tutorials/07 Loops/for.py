#!/usr/bin/python3
__author__ = "Santhosh Baswa"

def main():
    fh = open('lines.txt')
    for line in fh.readlines():
        print(line)

if __name__ == "__main__": main()
