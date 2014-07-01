#!/usr/bin/env python

from __future__ import division
from collections import defaultdict
import ConfigParser
import sys
import psycopg2cffi
import psycopg2cffi.extras

def comparision(virus, orgs, codon_table):
    ratio_scores = defaultdict(int)
    virus_ratio = compute_ratio(virus, codon_table)
    for org in orgs:
        id = org['id']
        org_ratio = compute_ratio(org, codon_table)
        for k in virus_ratio:
            ratio_scores[id] += abs(virus_ratio[k] - org_ratio[k])
    return ratio_scores

def compute_ratio(organism, codon_table):
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
                ratio = 0
            ratios[codon] = ratio
    return ratios

def dbconnect():
    config = ConfigParser.RawConfigParser()
    config.read('db.cfg')
    host = config.get('database', 'host')
    dbname = config.get('database', 'dbname')
    user = config.get('database', 'user')
    password = config.get('database', 'password')
    connection_string = 'host={host} dbname={dbname} user={user} password={password}'.format(**locals())
    conn = psycopg2cffi.connect(connection_string)
    return conn

def getCodonTable(cur):
    CODON_TABLE_SQL = "select acid,string_agg(codon, ' ') as codons from codon_table group by acid order by acid;"
    cur.execute(CODON_TABLE_SQL)
    return cur.fetchall()

def getVirus(cur):
    VIRUS_SQL = "select * from refseq where id = 'NG_027788.1';"
    cur.execute(VIRUS_SQL)
    return cur.fetchone()

def getOrganisms(cur, source):
    REFSEQ_SQL = "select * from "+ source + ";"
    cur.execute(REFSEQ_SQL)
    orgs = cur.fetchall()
    return orgs

def main(argv):
    conn = dbconnect()
    cur = conn.cursor(cursor_factory=psycopg2cffi.extras.DictCursor)
    codon_table = getCodonTable(cur)
    virus = getVirus(cur)
    orgs = getOrganisms(cur, 'refseq')

    results = comparision(virus, orgs, codon_table)
    for k in sorted(results, key=results.get):
        print results[k], k

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])
