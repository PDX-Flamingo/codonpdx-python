#!/usr/bin/env python

from __future__ import division
from collections import defaultdict
import sys
import datetime
from db import dbManager


# compare a virus to organisms in a sequence database
# db: the database manager used to get the data from
# virus_name: the accession and version number of the virus
# seq_db: the name of the sequence database table
# codon_table_name: the name of the codon table
def comparison(db, virus_name, seq_db, codon_table_name='standard'):
    virus = db.getOrganism(virus_name, seq_db)
    codon_table = db.getCodonTable(codon_table_name)
    scores = defaultdict(int)
    virus_ratio = ratio(virus, codon_table)
    for organism in db.getOrganisms(seq_db):
        organism_ratio = ratio(organism, codon_table)
        # calculate the score for the virus and this organism
        for k in virus_ratio:
            scores[organism['id']] += abs(virus_ratio[k] - organism_ratio[k])
    return scores


# calculate the ratios for a given organism using a certain codon table
# organism: the organism; needs be a dict that can map codon triplets to counts
# codon_table: the codon table acquired from a dbManager
def ratio(organism, codon_table):
    ratios = {}
    for acid, codons in codon_table:
        acid_total = 0
        # calculate the total number of codons for the acid
        for codon in codons.split(" "):
            acid_total += int(organism[codon.lower()])
        # calculate the number of each individual codon
        for codon in codons.split(" "):
            codon_total = int(organism[codon.lower()])
            if(codon_total != 0):
                ratio = codon_total / acid_total
            else:
                ratio = 0
            # store ratio for this codon
            ratios[codon] = ratio
    return ratios


def calc(args):
    time = datetime.datetime.now()
    db = dbManager('config/db.cfg')
    # do a comparison of virus 'NG_027788.1' with codon table 'standard'
    scores = comparison(db, args.virus, args.dbname, 'standard')
    # output if requested
    if args.output:
        print "Scores for " + args.virus + " versus " + args.dbname
        for k in sorted(scores, key=scores.get):
            print scores[k], k
    # otherwise put in the results table
    else:
        db.storeResults(args.virus, args.job, scores)
    db.commit()
