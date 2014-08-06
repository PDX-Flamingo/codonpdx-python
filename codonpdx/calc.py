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
    virus_shuffle_ratio = ratio_shuffle(virus, codon_table)
    for organism in db.getOrganisms(seq_db):
        organism_ratio = ratio(organism, codon_table)
        # calculate the score for the virus and this organism
        for k in virus_ratio:
            scores[organism['id']] += abs(virus_ratio[k] - organism_ratio[k])
        for k in virus_shuffle_ratio:
            shuffle_scores[organism['id']] += \
                abs(virus_shuffle_ratio[k] - organism_ratio[k])
    return [scores, shuffle_scores]


# same as above but takes a list of accession ids to use from the table
def comparison_list(db, virus_name, virus_db, ids, seq_db, codon_table_name):
    virus = db.getOrganism(virus_name, virus_db)
    codon_table = db.getCodonTable(codon_table_name)
    scores = defaultdict(int)
    shuffle_scores = defaultdict(int)
    virus_ratio = ratio(virus, codon_table)
    virus_shuffle_ratio = ratio_shuffle(virus, codon_table)
    # this portion is the only changed part; get subset instead of everything
    # maybe consider passing None as the id list and getting everything in
    # case so we don't have to have a whole separate method for this option
    for organism in db.getOrganismSubset(ids, seq_db):
        organism_ratio = ratio(organism, codon_table)
        # calculate the score for the virus and this organism
        for k in virus_ratio:
            scores[organism['id']] += abs(virus_ratio[k] - organism_ratio[k])
        for k in virus_shuffle_ratio:
            shuffle_scores[organism['id']] += \
                abs(virus_shuffle_ratio[k] - organism_ratio[k])
    return [scores, shuffle_scores]


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
            # normal sequence codons
            codon_total = int(organism[codon.lower()])
            if codon_total != 0:
                ratio_calc = codon_total / acid_total
            else:
                ratio_calc = 0
            # ratio for this codon
            ratios[codon] = ratio_calc
    return ratios


# as shuffle(), but for organisms with shuffle fields
def ratio_shuffle(organism, codon_table):
    ratios = {}
    for acid, codons in codon_table:
        acid_total = 0
        # calculate the total number of codons for the acid
        for codon in codons.split(" "):
            acid_total += int(organism["shuffle_" + codon.lower()])
        # calculate the number of each individual codon
        for codon in codons.split(" "):
            # normal sequence codons
            codon_total = int(organism["shuffle_" + codon.lower()])
            if codon_total != 0:
                ratio_calc = codon_total / acid_total
            else:
                ratio_calc = 0
            # ratio for this codon
            ratios[codon] = ratio_calc
    return ratios


def calc(args):
    with dbManager('config/db.cfg') as db:
        # do custom list comparison if we have an id list
        if hasattr(args, 'ids'):
            scores_calc = comparison_list(db, args.job, 'input',
                                          args.ids, args.dbname, 'standard')
        else:
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
            db.storeResults(args.job, scores_calc[0], scores_calc[1])
