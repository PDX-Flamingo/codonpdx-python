#!/usr/bin/env python

from __future__ import division
from collections import defaultdict
import ConfigParser
import sys
import psycopg2cffi
import psycopg2cffi.extras
import datetime


class dbManager:
    'Handles the database connection used by the calculator'

    # constructor
    # conf: name of the config file to use to connect to the database
    #  Should be an ini file with a section called "database" with three
    #  properties:
    #   "host": the host name
    #   "dbname": the database name
    #   "user": the name of the user to log in as
    #   "password": the password to log in with
    def __init__(self, conf):
        # read config file to get connection information
        config = ConfigParser.RawConfigParser()
        config.read(conf)
        host = config.get('database', 'host')
        dbname = config.get('database', 'dbname')
        user = config.get('database', 'user')
        password = config.get('database', 'password')
        connection_string = 'host={host} dbname={dbname} user={user} \
                             password={password}'.format(**locals())
        # set up connection and cursor members
        self.conn = psycopg2cffi.connect(connection_string)
        self.cur = self.conn.cursor(
            cursor_factory=psycopg2cffi.extras.DictCursor
        )

    # on garbage collect, close connections if the user forgot to do so
    def __del__(self):
        self.close()

    # for with-as statements; do nothing special on entry
    def __enter__(self):
        return self

    # but close the connection when exiting that scope
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # call this when finished with the connection
    def close(self):
        # complete db transaction
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    # get a virus from a sequence database
    # virus: the accession and version number of the virus
    # source: the sequence database to get the virus from
    def getOrganism(self, name, source):
        self.cur.execute("SELECT * FROM "+source+" "
                         "WHERE id=(%s);",
                         (name,))
        return self.cur.fetchone()

    # acuqire all the organisms from a sequence database
    # source: the name of the sequence database (e.g., 'refseq')
    #  This string is used directly in the query and needs to be safe
    def getOrganisms(self, source):
        self.cur.execute("SELECT * FROM "+source+";")
        return self.cur.fetchall()

    # get a codon <-> acid translation table
    # kind: the name of the table to acquire
    #  This string is used directly in the query and needs to be safe
    def getCodonTable(self, kind='standard'):
        self.cur.execute("SELECT acid,string_agg(codon, ' ')"
                         "AS codons "
                         "FROM codon_table "
                         "WHERE name=(%s) "
                         "GROUP BY acid "
                         "ORDER BY acid;",
                         (kind,))
        return self.cur.fetchall()

    # insert an organism into a table
    # org: dictionary describing the organism
    # table: what table to insert the organism into
    # job: the job uuid; used in the case of inserting into input
    def insertOrganism(self, org, table, job):
        insert = "INSERT INTO " + table + " "
        cols = "(id, taxonomy, description, time"
        vals = "VALUES (%s, %s, %s, %s"
        data = [
            org['id'] if table != 'input' else job,
            org['taxonomy'],
            org['description'],
            datetime.datetime.utcnow()
        ]
        for codon, count in org['codoncount'].iteritems():
            cols += ", " + codon
            vals += ", %s"
            data.append(count)
        cols += ") "
        vals += ");"
        self.cur.execute(insert + cols + vals, tuple(data))

    # insert an organism into a table
    # org: dictionary describing the organism
    # table: what table to insert the organism into
    # job: the job uuid; used in the case of inserting into input
    def insertInputOrganism(self, org, table, job):
        insert = "INSERT INTO " + table + " "
        cols = "(id, taxonomy, description, time"
        vals = "VALUES (%s, %s, %s, %s"
        data = [
            org['id'] if table != 'input' else job,
            org['taxonomy'],
            org['description'],
            datetime.datetime.utcnow()
        ]
        for codon, count in org['codoncount'].iteritems():
            cols += ", " + codon
            vals += ", %s"
            data.append(count)
        for shuffle_codon, count in org['shufflecodoncount'].iteritems():
            cols += ", " + "shuffle_" + shuffle_codon
            vals += ", %s"
            data.append(count)
        cols += ") "
        vals += ");"
        self.cur.execute(insert + cols + vals, tuple(data))

    # take the results of a comparison operation and store them in the
    # results table
    # job_uuid: datetime of when the comparison started
    # scores: map from organism id -> comparison score
    def storeResults(self, job_uuid, scores):
        for org2 in scores:
            self.cur.execute(
                "INSERT INTO results "
                "(job_uuid,organism2,score,time) "
                "VALUES (%s,%s,%s,%s);",
                (job_uuid, org2, scores[org2], datetime.datetime.utcnow()))

    # clear data from a table
    # table: name of the table
    def truncateTable(self, table):
        self.cur.execute("TRUNCATE " + table + ";")
