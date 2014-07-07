import json

from ctypes import *
from CodonCountStruct import CodonCount

from Bio import SeqIO


def getdict(struct):
    return dict(
        (field, getattr(struct, field)) for field, _ in struct._fields_
        )


def writeCounts(data, pretty):
    if pretty:
        sort = True
        ident = 2
    else:
        sort = False
        ident = None

    if data:
        print json.dumps(data, sort_keys=sort, indent=ident)


def codonCount(args):
    counterc = CDLL('./lib/counterc.so')
    counterc.countcodons.argtypes = (c_char_p,)
    counterc.countcodons.restype = CodonCount

    data = []

    for seq_record in SeqIO.parse(args.infile, args.format):
        if len(seq_record.seq) != seq_record.seq.count("N"):
            cstruct = counterc.countcodons(str(seq_record.seq))
            data += [{
                     "id": seq_record.id,
                     "name": seq_record.name,
                     "description": seq_record.description,
                     "annotations": str(seq_record.annotations),
                     "features": str(seq_record.features),
                     "dbxrefs": seq_record.dbxrefs,
                     "codoncount": getdict(cstruct)
                     }]
    writeCounts(data, args.pretty)
