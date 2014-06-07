from collections import Counter
from Bio import SeqIO
from Bio.SeqUtils import GC
#for seq_record in SeqIO.parse("/home/blkperl/Downloads/cow.rna.fna", "fasta"):
for seq_record in SeqIO.parse("samples/test.fasta", "fasta"):
    print seq_record.id
    cnt = Counter()
    line = seq_record.seq
    n = 3
    for acid in [line[i:i+n] for i in range(0, len(line), n)]:
      cnt[str(acid)] += 1
    print cnt


