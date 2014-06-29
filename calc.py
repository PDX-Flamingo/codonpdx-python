#!/usr/bin/env python

from __future__ import division
from collections import defaultdict
import ConfigParser
import sys
import psycopg2
import psycopg2.extras

def comparision(virus, orgs):
    ratio_scores = defaultdict(int)
    virus_ratio = compute_ratio(virus)
    for org in orgs:
        id = org['description']
        org_ratio = compute_ratio(org)
        for k in virus_ratio:
            ratio_scores[id] += abs(virus_ratio[k] - org_ratio[k])
    return ratio_scores

def compute_ratio(organism):
    ratios = {}
    for acid,codons in codon_table:
        acid_count = 0
        for codon in codons.split(" "):
            acid_count += int(organism[codon.lower()])
        for codon in codons.split(" "):
            codon_count = int(organism[codon.lower()])
            if (codon_count != 0):
                ratio = codon_count / acid_count
            else:
                ratio = 1
            ratios[codon] = ratio
    return ratios

config = ConfigParser.RawConfigParser()
config.read('db.cfg')

host = config.get('database', 'host')
dbname = config.get('database', 'dbname')
user = config.get('database', 'user')
password = config.get('database', 'password')

connection_string = 'host={host} dbname={dbname} user={user} password={password}'.format(**locals())
conn = psycopg2.connect(connection_string)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
CODON_TABLE_SQL = "select acid,string_agg(codon, ' ') as codons from codon_table group by acid order by acid;"
REFSEQ_SQL = "select * from refseq;"
VIRUS_SQL = "select * from refseq where id = 'NG_027788.1';"
cur.execute(CODON_TABLE_SQL)
codon_table = cur.fetchall()
cur.execute(REFSEQ_SQL)
orgs = cur.fetchall()
cur.execute(VIRUS_SQL)
virus = cur.fetchone()

results = comparision(virus, orgs)
for k in sorted(results, key=results.get):
    print results[k], k

conn.commit()
cur.close()
conn.close()

