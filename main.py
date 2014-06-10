#!/usr/bin/python

import getopt
import sys
import count


def main(argv):
    inputfile = sys.stdin
    format = 'fasta'
    try:
        opts, args = getopt.getopt(argv, "hi:f:", ["ifile=", "format="])
    except getopt.GetoptError:
        print ('count.py -i <inputfile> -f <format>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('count.py -i <inputfile> -f <format>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-f", "--format"):
            format = arg
    print ('Input file is', inputfile)

    count.compute(inputfile, format)

if __name__ == "__main__":
    main(sys.argv[1:])
