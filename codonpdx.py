#!/usr/bin/env python

import argparse
import sys
from codonpdx.calc import calcScore
from codonpdx.count import codonCount
from codonpdx.db import loadDB

# create the top-level parser
parser = argparse.ArgumentParser(prog='codonpdx',
                                 description='codonpdx command line util')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "count" command
parserCount = subparsers.add_parser('count', help='codon counter')
parserCount.add_argument('-i', '--infile', nargs='?',
                         type=argparse.FileType('r'), default=sys.stdin,
                         help='a file path')
parserCount.add_argument('-f', '--format', choices=['fasta', 'genbank'],
                         help='the file format')
parserCount.add_argument('-p', '--pretty', action='store_true',
                         help='enable json pretty print')
parserCount.set_defaults(func=codonCount)

# create the parser for the "loadDB" command
parserLoadDB = subparsers.add_parser('loadDB',
                                     help='stores codon count metadata')
parserLoadDB.add_argument('-d', '--dbname', choices=['refseq', 'genbank'],
                          help='the dbname to store the count metadata')
parserLoadDB.add_argument('-i', '--infile', nargs='?',
                          type=argparse.FileType('r'), default=sys.stdin,
                          help='a file path')
parserLoadDB.set_defaults(func=loadDB)


# create the parser for the "calcScore" command
parserCalcScore = subparsers.add_parser(
    'calcScore',
    help='calculate the codon count scores'
)
parserCalcScore.add_argument('-d', '--dbname', choices=['refseq', 'genbank'],
                             help='the dbname to fetch the count metadata')
parserCalcScore.add_argument('-v', '--virus', required=True,
                             help='the virus id to compare against')
parserCalcScore.set_defaults(func=calcScore)

args = parser.parse_args()
args.func(args)
