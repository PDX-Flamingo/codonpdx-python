#!/usr/bin/env python

import argparse
import codonpdx.calc
import codonpdx.count
import codonpdx.insert
import codonpdx.mirror
import codonpdx.queueJobs
import sys

# create the top-level parser
parser = argparse.ArgumentParser(prog='codonpdx',
                                 description='Codonpdx command line utility.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
subparsers = parser.add_subparsers(help='Sub-command descriptions:')

# create the parser for the "count" command
parserCount = subparsers.add_parser(
    'count',
    help='Count the codons of a file and produce JSON '
         'output containing the results.'
)
parserCount.add_argument(
    '-i',
    '--infile',
    nargs='?',
    type=argparse.FileType('r'),
    default=sys.stdin,
    help='A file containing sequence data.'
)
parserCount.add_argument(
    '-g',
    '--gzip',
    action='store_true',
    default=False,
    help='Indicates the input is gzipped.'
)
parserCount.add_argument(
    '-j',
    '--job',
    required=True,
    help='The UUID for the job if this process is placing its results into '
         'the results table.'
)
parserCount.add_argument(
    '-f',
    '--format',
    choices=['fasta', 'genbank'],
    help='The file format.'
)
parserCount.add_argument(
    '-p',
    '--pretty',
    action='store_true',
    help='Print the JSON in a pretty, more human-readable way.'
)
parserCount.add_argument(
    '-o',
    '--output',
    nargs='?',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='Where to place the output JSON.'
)
parserCount.set_defaults(
    func=codonpdx.count.count
)

# create the parser for the "insert" command
parserLoadDB = subparsers.add_parser(
    'insert',
    help='Insert organism codon count JSON information into the database.'
)
parserLoadDB.add_argument(
    '-d',
    '--dbname',
    choices=['refseq', 'genbank', 'input'],
    help='The database table to store the count information in.'
)
parserLoadDB.add_argument(
    '-i',
    '--infile',
    nargs='?',
    type=argparse.FileType('r'),
    default=sys.stdin,
    help='The file to to read the JSON data from. Defaults to standard input.'
)
parserLoadDB.add_argument(
    '-j',
    '--job',
    required=True,
    help='The UUID for the job if this process is placing its results into '
         'the results table.'
)
parserLoadDB.set_defaults(
    func=codonpdx.insert.insert
)

# create the parser for the "calc" command
parserCalcScore = subparsers.add_parser(
    'calc',
    help='Compare an organism to all other organisms in a given sequence '
         'database.'
)
parserCalcScore.add_argument(
    '-d',
    '--dbname',
    choices=['refseq', 'genbank'],
    help='The sequence database to compare the organism to.'
)
parserCalcScore.add_argument(
    '-v',
    '--virus',
    required=True,
    help='The accession.version number of the organism to compare.'
)
parserCalcScore.add_argument(
    '-w',
    '--virusdb',
    choices=['input', 'refseq', 'genbank'],
    default='input',
    help='The database table where the input virus resides.'
)
parserCalcScore.add_argument(
    '-o',
    '--output',
    action='store_true',
    help='Output scores to stdout instead of storing in the results table.'
)
parserCalcScore.add_argument(
    '-j',
    '--job',
    required=True,
    help='The UUID for the job if this process is placing its results into '
         'the results table.'
)
parserCalcScore.set_defaults(
    func=codonpdx.calc.calc
)

# create the mirror subcommand
parserMirror = subparsers.add_parser(
    'mirror',
    help='Mirror remote codon repository'
)
parserMirror.add_argument(
    '-d',
    '--dbname',
    required=True,
    choices=['refseq', 'genbank'],
    help='The repository to mirror'
)

parserMirror.set_defaults(
    func=codonpdx.mirror.mirror
)

# create the queueJobs subcommand
parserQueueJobs = subparsers.add_parser(
    'queueJobs',
    help='Count and load repository codon counts into postgres'
)
parserQueueJobs.add_argument(
    '-d',
    '--dbname',
    required=True,
    choices=['refseq', 'genbank'],
    help='The repository to parse'
)
parserQueueJobs.add_argument(
    '-f',
    '--format',
    choices=['fasta', 'genbank'],
    help='The file format.'
)

parserQueueJobs.set_defaults(
    func=codonpdx.queueJobs.queueJobs
)

args = parser.parse_args()
args.func(args)
