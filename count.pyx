#!/usr/bin/python

import json
from Bio import SeqIO


def compute(inputfile):
  cdef str line = ''
  cdef int i = 0
  cdef int j = 0
  cdef int line_len = 0
  cdef str token = ''
  cdef int token_cnt = 0
  for seq_record in SeqIO.parse(inputfile, "fasta"):
      cnt = {}
      line = str(seq_record.seq)
      line_len = len(line)
      for j in xrange(line_len / 3):
        i = j * 3
        token = line[i:i+3]
        try:
          token_cnt = cnt[token]
        except KeyError:
          cnt[token] = 1
        else:
          cnt[token] = token_cnt + 1
      print json.dumps(
        [{
        "id"          : seq_record.id,
        "ratios"      : cnt
        }])

