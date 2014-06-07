from collections import Counter
from Bio import SeqIO
from Bio.SeqUtils import GC
for seq_record in SeqIO.parse("samples/test.fasta", "fasta"):
    print seq_record.id
    cnt = Counter()
    line = seq_record.seq
    n = 3
    for codon in [line[i:i+n] for i in range(0, len(line), n)]:
      cnt[str(codon)] += 1
    print cnt


