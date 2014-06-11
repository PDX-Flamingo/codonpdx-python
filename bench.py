# !/usr/bin/python

import sys
import time

from ctypes import *
from CodonCountStruct import CodonCount

""" Utility """
CURRENT_MILLI_TIME = lambda: int(round(time.clock() * 1000))


def getdict(struct):
    return dict((field, getattr(struct, field)) for field, _ in struct._fields_)

def main(argv):
    counterc = CDLL('./counterc.so')
    counterc.countcodons.argtypes = (c_char_p,)
    counterc.countcodons.restype = CodonCount

    start = CURRENT_MILLI_TIME()

    for line in sys.stdin:
        cstruct = counterc.countcodons(line)
    print getdict(cstruct)

    end = CURRENT_MILLI_TIME()
    print "Tokenize and Count in " + str(end - start) + " ms"


if __name__ == "__main__":
    main(sys.argv[1:])
