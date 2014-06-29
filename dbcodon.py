#!/usr/bin/env python


import ConfigParser
import sys, json
import psycopg2

config = ConfigParser.RawConfigParser()
config.read('db.cfg')

host = config.get('database', 'host')
dbname = config.get('database', 'dbname')
user = config.get('database', 'user')
password = config.get('database', 'password')

data = json.load(sys.stdin)
connection_string = 'host={host} dbname={dbname} user={user} password={password}'.format(**locals())
conn = psycopg2.connect(connection_string)
cur = conn.cursor()
SQL = "INSERT INTO refseq (id, name, description, ACT, ACG, ACA, ACC, ATC, ATG, ATA, ATT, AGC, AGT, AGA, AGG, AAC, AAT, AAG, AAA, CAT, CAG, CAA, CAC, CTA, CTG, CTC, CTT, CGA, CGT, CGC, CGG, CCA, CCT, CCG, CCC, TAC, TAG, TAA, TAT, TCA, TCG, TCC, TCT, TGA, TGC, TGT, TGG, TTA, TTC, TTG, TTT, GAC, GAT, GAA, GAG, GCA, GCT, GCC, GCG, GTA, GTC, GTT, GTG, GGA, GGC, GGT, GGG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

for org in data:
    id = str(org['id'])
    name = str(org['name'])
    desc = str(org['description'])
    cc = org['codoncount']
    cur.execute(SQL, (id,name,desc, int(cc['AAA']),int(cc['AAC']),int(cc['AAG']),int(cc['AAT']),int(cc['ACA']),int(cc['ACC']),int(cc['ACG']),int(cc['ACT']),int(cc['AGA']),int(cc['AGC']),int(cc['AGG']),int(cc['AGT']),int(cc['ATA']),int(cc['ATC']),int(cc['ATG']),int(cc['ATT']),int(cc['CAA']),int(cc['CAC']),int(cc['CAG']),int(cc['CAT']),int(cc['CCA']),int(cc['CCC']),int(cc['CCG']),int(cc['CCT']),int(cc['CGA']),int(cc['CGC']),int(cc['CGG']),int(cc['CGT']),int(cc['CTA']),int(cc['CTC']),int(cc['CTG']),int(cc['CTT']),int(cc['GAA']),int(cc['GAC']),int(cc['GAG']),int(cc['GAT']),int(cc['GCA']),int(cc['GCC']),int(cc['GCG']),int(cc['GCT']),int(cc['GGA']),int(cc['GGC']),int(cc['GGG']),int(cc['GGT']),int(cc['GTA']),int(cc['GTC']),int(cc['GTG']),int(cc['GTT']),int(cc['TAA']),int(cc['TAC']),int(cc['TAG']),int(cc['TAT']),int(cc['TCA']),int(cc['TCC']),int(cc['TCG']),int(cc['TCT']),int(cc['TGA']),int(cc['TGC']),int(cc['TGG']),int(cc['TGT']),int(cc['TTA']),int(cc['TTC']),int(cc['TTG']),int(cc['TTT'])))


conn.commit()
cur.close()
conn.close()
