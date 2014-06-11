#!/usr/bin/python

import getopt
import json
import sys

from ctypes import *
from CodonCountStruct import CodonCount

from Bio import SeqIO


def getdict(struct):
    return dict((field, getattr(struct, field)) for field, _ in struct._fields_)


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

    counterc = CDLL('./counterc.so')
    counterc.countcodons.argtypes = (c_char_p,)
    counterc.countcodons.restype = CodonCount

    for seq_record in SeqIO.parse(inputfile, format):
        if len(seq_record.seq) != seq_record.seq.count("N"):
            cstruct = counterc.countcodons(str(seq_record.seq))
            data = [{
                        "id": seq_record.id,
                        "name": seq_record.name,
                        "description": seq_record.description,
                        "annotations": str(seq_record.annotations),
                        "features": str(seq_record.features),
                        "dbxrefs": seq_record.dbxrefs,
                        "codoncount": getdict(cstruct)
                    }]
            print json.dumps(data, sort_keys=True, indent=2)


if __name__ == "__main__":
    main(sys.argv[1:])
