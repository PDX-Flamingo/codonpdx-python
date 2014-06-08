import json

from collections import Counter
from Bio import SeqIO
from Bio.SeqUtils import GC
for seq_record in SeqIO.parse("samples/test.fasta", "fasta"):
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

