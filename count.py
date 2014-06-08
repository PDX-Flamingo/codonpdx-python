#!/usr/bin/python

import getopt
import json
import sys
from collections import Counter
from Bio import SeqIO
from Bio.SeqUtils import GC


def compute(inputfile):
  for seq_record in SeqIO.parse(inputfile, "fasta"):
      cnt = Counter()
      line = str(seq_record.seq)
      i = 0
      for j in range(((len(line))/ 3)):
        cnt[line[i:i+3]] += 1
        i += 3
      print json.dumps(
        [{
        "id"          : seq_record.id,
        "ratios"      : cnt
        }], sort_keys=True, indent=4, separators=(',', ': '))

def main(argv):
   inputfile = 'samples/test.fasta'
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'count.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'count.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print 'Input file is', inputfile

   compute(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
