import gzip
import json
import Bio
import Bio.SeqIO

from ctypes import *
from CodonCountStruct import CodonCount


# convert ctypes structure into a python dictionary
def getdict(struct):
    return dict(
        (field, getattr(struct, field)) for field, _ in struct._fields_
        )


# produce JSON from data object
def writeCounts(data, pretty):
    if pretty:
        sort = True
        ident = 2
    else:
        sort = False
        ident = None
    return json.dumps(data, sort_keys=sort, indent=ident)


# count codons and produce json containing the organism information & counts
# args.infile = path to a file to parse
# args.format = 'fasta' or 'genbank', the format of the file
# args.pretty = boolean, whether or not to pretty-print the resulting JSON
# args.output = file to output the JSON to
def count(args):
    counterc = CDLL('./lib/counterc.so')
    counterc.countcodons.argtypes = (c_char_p,)
    counterc.countcodons.restype = CodonCount

    data = []

    if args.gzip:
        handle = gzip.GzipFile(fileobj=args.infile)
    else:
        handle = args.infile

    for seq_record in Bio.SeqIO.parse(handle, args.format):
        # only bother producing output if there is actual sequence data;
        # i.e., not all unknowns
        if len(seq_record.seq) != seq_record.seq.count("N"):
            # count the codons and put them in the data object along with
            # other metadata
            cstruct = counterc.countcodons(str(seq_record.seq))
            # get taxonomy information
            tax = ""
            if 'taxonomy' in seq_record.annotations:
                tax = '; '.join(seq_record.annotations['taxonomy'])
            # add the sequence information into our results
            data += [{
                # accession.version if we have a genbank file
                # otherwise we should use the job uuid
                "id": args.job if args.format == 'fasta' else seq_record.id,
                # taxonomy information
                "taxonomy": tax,
                "description": seq_record.description,
                "codoncount": getdict(cstruct)
            }]
    # only write if data exists (i.e., we actually had sequence data
    if data:
        json = writeCounts(data, args.pretty)
        if args.output:
            args.output.write(json)
        return json
