#!/usr/bin/env python


import sys, json
import psycopg2

data = json.load(sys.stdin)
conn = psycopg2.connect("host=localhost dbname=pdxcodon user=pdxcodon password=secret")
cur = conn.cursor()
REFSEQ_SQL = "INSERT INTO refseq (pid, id, name, description) VALUES (%s, %s, %s, %s);"
REFSEQ_COUNT_SQL = "INSERT INTO refseq_counts (refseq_id, codon, count) VALUES (%s, %s, %s);"
cur.execute("SELECT nextval('refseq_id');")
refseq_id = int(cur.fetchone()[0])

print "refseq id is", refseq_id

for org in data:
    name = str(org['name'])
    id = str(org['id'])
    desc = str(org['description'])
    cur.execute(REFSEQ_SQL, (refseq_id,id,name,desc))
    for k,v in org['codoncount'].items():
        cur.execute(REFSEQ_COUNT_SQL, (refseq_id,k,int(v)))


conn.commit()
cur.close()
conn.close()
