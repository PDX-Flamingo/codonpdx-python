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
REFSEQ_SQL = "INSERT INTO refseq (pid, id, name, description) VALUES (%s, %s, %s, %s);"
REFSEQ_COUNT_SQL = "INSERT INTO refseq_counts (refseq_id, codon, count) VALUES (%s, %s, %s);"

for org in data:
    cur.execute("SELECT nextval('refseq_id');")
    refseq_id = int(cur.fetchone()[0])
    name = str(org['name'])
    id = str(org['id'])
    desc = str(org['description'])
    cur.execute(REFSEQ_SQL, (refseq_id,id,name,desc))
    for k,v in org['codoncount'].items():
        cur.execute(REFSEQ_COUNT_SQL, (refseq_id,k,int(v)))


conn.commit()
cur.close()
conn.close()
