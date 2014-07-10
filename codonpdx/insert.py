#!/usr/bin/env python

import ConfigParser
import json
import psycopg2cffi
import psycopg2cffi.extras
import sys


# get db connection object (use dbManager)
def connectToDb():
    config = ConfigParser.RawConfigParser()
    config.read('config/db.cfg')

    host = config.get('database', 'host')
    dbname = config.get('database', 'dbname')
    user = config.get('database', 'user')
    password = config.get('database', 'password')

    connection_string = 'host={host} dbname={dbname} user={user} \
                         password={password}'.format(**locals())
    conn = psycopg2cffi.connect(connection_string)
    return conn


# get codon table (use dbManager)
def getCodons(cur):
    sql = "select string_agg(codon, ' ') as codons from codon_table \
           where name = 'standard';"
    cur.execute(sql)
    return cur.fetchone()['codons']


# make format string for inserting organism into database
def buildSQLStmt(cur, dbname):
    sql = "INSERT INTO " + dbname + "(id, name, description"
    startStmt = ""
    endStmt = ") VALUES ("
    codons = sorted(getCodons(cur).split(" "))
    for codon in codons:
        startStmt += ", " + codon
        endStmt += "%s, "

    return sql + startStmt + endStmt + "%s, %s, %s);"


# read organism data from JSON and insert into database
def insertCounts(data, cur, dbname):
    for org in data:
        id = str(org['id'])
        name = str(org['name'])
        desc = str(org['description'])
        cc = org['codoncount']
        cur.execute(
            buildSQLStmt(cur, dbname),
            (id, name, desc,  int(cc['AAA']), int(cc['AAC']), int(cc['AAG']),
             int(cc['AAT']), int(cc['ACA']), int(cc['ACC']), int(cc['ACG']),
             int(cc['ACT']), int(cc['AGA']), int(cc['AGC']), int(cc['AGG']),
             int(cc['AGT']), int(cc['ATA']), int(cc['ATC']), int(cc['ATG']),
             int(cc['ATT']), int(cc['CAA']), int(cc['CAC']), int(cc['CAG']),
             int(cc['CAT']), int(cc['CCA']), int(cc['CCC']), int(cc['CCG']),
             int(cc['CCT']), int(cc['CGA']), int(cc['CGC']), int(cc['CGG']),
             int(cc['CGT']), int(cc['CTA']), int(cc['CTC']), int(cc['CTG']),
             int(cc['CTT']), int(cc['GAA']), int(cc['GAC']), int(cc['GAG']),
             int(cc['GAT']), int(cc['GCA']), int(cc['GCC']), int(cc['GCG']),
             int(cc['GCT']), int(cc['GGA']), int(cc['GGC']), int(cc['GGG']),
             int(cc['GGT']), int(cc['GTA']), int(cc['GTC']), int(cc['GTG']),
             int(cc['GTT']), int(cc['TAA']), int(cc['TAC']), int(cc['TAG']),
             int(cc['TAT']), int(cc['TCA']), int(cc['TCC']), int(cc['TCG']),
             int(cc['TCT']), int(cc['TGA']), int(cc['TGC']), int(cc['TGG']),
             int(cc['TGT']), int(cc['TTA']), int(cc['TTC']), int(cc['TTG']),
             int(cc['TTT']))
        )


def insert(args):
    data = json.load(args.infile)
    conn = connectToDb()
    cur = conn.cursor(cursor_factory=psycopg2cffi.extras.DictCursor)
    insertCounts(data, cur, args.dbname)
    conn.commit()
    cur.close()
    conn.close()
