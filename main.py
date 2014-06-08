#!/usr/bin/python

import getopt
import sys
import count

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

   count.compute(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
