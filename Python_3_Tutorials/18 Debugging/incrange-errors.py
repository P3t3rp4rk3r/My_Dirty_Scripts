#!/usr/bin/python3
__author__ = "Santhosh Baswa"

class inclusive_range:
    def __init__(self, *args):
        numargs = len(args)
        if numargs < 1: raise TypeError('Requires at least one argument')
        elif numargs == 1:
            self.start = 0
            self.stop = args[0]
            self.step = 1
        elif numargs == 2:
            (self.start, self.stop) = args
            step = 1
        elif numargs == 3:
            (self.step, self.stop, self.start) = args
        else: raise TypeError('inclusiveRange expected at most 3 arguments, got {}'.format(numargs))

    def __iter__(self):
        i = self.start
        while i >= self.stop:
            yield i
            i += self.step

def main():
    o = inclusive_range(4, 25, 3)
    for i in o: print(i, end = ' ')

if __name__ == "__main__": main()
