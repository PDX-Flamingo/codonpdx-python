#!/usr/bin/env python

import argparse
import sys
from codonpdx.calc import calcScore
from codonpdx.count import codonCount
from codonpdx.insert import loadDB

# create the top-level parser
parser = argparse.ArgumentParser(prog='codonpdx',
                                 description='Codonpdx command line utility.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
subparsers = parser.add_subparsers(help='Sub-command descriptions:')

# create the parser for the "count" command
parserCount = subparsers.add_parser('count', help='Count the codons of a file and produce JSON output containing the results.')
parserCount.add_argument('-i', '--infile', nargs='?',
                         type=argparse.FileType('r'), default=sys.stdin,
                         help='A file containing sequence data.')
parserCount.add_argument('-f', '--format', choices=['fasta', 'genbank'],
                         help='The file format.')
parserCount.add_argument('-p', '--pretty', action='store_true',
                         help='Print the JSON in a pretty, more human-readable way.')
parserCount.set_defaults(func=codonCount)

# create the parser for the "loadDB" command
parserLoadDB = subparsers.add_parser('insert',
                                     help='Insert organism codon count JSON information into the database.')
parserLoadDB.add_argument('-d', '--dbname', choices=['refseq', 'genbank'],
                          help='The database table to store the count information in.')
parserLoadDB.add_argument('-i', '--infile', nargs='?',
                          type=argparse.FileType('r'), default=sys.stdin,
                          help='The file to to read the JSON data from. Defaults to standard input.')
parserLoadDB.set_defaults(func=loadDB)


# create the parser for the "calcScore" command
parserCalcScore = subparsers.add_parser(
    'calc',
    help='Compare an organism to all other organisms in a given sequence database.'
)
parserCalcScore.add_argument('-d', '--dbname', choices=['refseq', 'genbank'],
                             help='The sequence database to compare the organism to.')
parserCalcScore.add_argument('-v', '--virus', required=True,
                             help='The accession.version number of the organism to compare. (Currently must be located in the sequence database to compare against.)')
parserCalcScore.set_defaults(func=calcScore)

args = parser.parse_args()
args.func(args)
