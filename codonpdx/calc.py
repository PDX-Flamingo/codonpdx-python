#!/usr/bin/env python

from __future__ import division
from collections import defaultdict
from db import dbManager


# compare a virus to organisms in a sequence database
# db: the database manager used to get the data from
# virus_name: the accession and version number of the virus
# virus_db: the location of the input virus's information (probably 'input')
# seq_db: the name of the sequence database table
# codon_table_name: the name of the codon table
def comparison(db, virus_name, virus_db, seq_db, codon_table_name):
    virus = db.getOrganism(virus_name, virus_db)
    codon_table = db.getCodonTable(codon_table_name)
    scores = defaultdict(int)
    shuffle_scores = defaultdict(int)
    virus_ratio = ratio(virus, codon_table)
    for organism in db.getOrganisms(seq_db):
        organism_ratio = ratio(organism, codon_table)
        # calculate the score for the virus and this organism
        for k in virus_ratio[0]:
            scores[organism['id']] += abs(virus_ratio[0][k] - organism_ratio[k])
        for k in virus_ratio[1]:
            shuffle_scores[organism['id']] = abs(virus_ratio[1][k] - organism_ratio[k])
    return [scores, shuffle_scores]


# calculate the ratios for a given organism using a certain codon table
# organism: the organism; needs be a dict that can map codon triplets to counts
# codon_table: the codon table acquired from a dbManager
def ratio(organism, codon_table):
    ratios = {}
    shuffle_ratios = {}
    for acid, codons in codon_table:
        acid_total = 0
        # calculate the total number of codons for the acid
        for codon in codons.split(" "):
            acid_total += int(organism[codon.lower()])
            shuffle_acid_total += int(organism["shuffle_" + codon.lower()])
        # calculate the number of each individual codon
        for codon in codons.split(" "):
            # normal sequence codons
            codon_total = int(organism[codon.lower()])
            if(codon_total != 0):
                ratio_calc = codon_total / acid_total
            else:
                ratio_calc = 0
            # calculate the number of codons in the shuffle
            shuffle_codon_total = int(organism["shuffle_" + codon.lower()])
            if(shuffle_codon_total != 0):
                shuffle_ratio_calc = shuffle_codon_total / shuffle_acid_total
            else:
                shuffle_ratio_calc = 0
            # ratio for this codon
            ratios[codon] = ratio_calc
            # ratio for this codon in the shuffle sequence
            shuffle_ratios[codon.lower()] = shuffle_ratio_calc
    return [ratios, shuffle_ratios]


def calc(args):
    with dbManager('config/db.cfg') as db:
        # do a comparison of virus 'NG_027788.1' with codon table 'standard'
        scores_calc = comparison(db, args.job, 'input',
                                 args.dbname, 'standard')
        # output if requested
        if args.output:
            print "Scores for " + args.virus + " versus " + args.dbname
            for k in sorted(scores_calc[0], key=scores_calc[0].get):
                print scores_calc[0][k], k
            print "Shuffle scores for " + args.virus + " versus " + args.dbname
            for k in sorted(scores_calc[1], key=scores_calc[1].get):
                print scores_calc[1][k], k
            
        # otherwise put in the results table
        else:
            db.storeResults(args.job, scores_calc)
