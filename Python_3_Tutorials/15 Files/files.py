#!/usr/bin/python3
__author__ = "Santhosh Baswa"

def main():
    f = open('lines.txt')
    for line in f:
        print(line, end = '')

if __name__ == "__main__": main()
