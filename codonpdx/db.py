#!/usr/bin/env python

from __future__ import division
from collections import defaultdict
import ConfigParser
import sys
import psycopg2cffi
import psycopg2cffi.extras


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
        self.cur = self.conn.cursor(cursor_factory=psycopg2cffi.extras.DictCursor)

    # destructor
    def __del__(self):
        # complete db transaction
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    # get a virus from a sequence database
    # virus: the accession and version number of the virus
    # source: the sequence database to get the virus from
    def getOrganism(self, name, source):
        self.cur.execute("SELECT * FROM "+source+" " +
                         "WHERE id=(%s);", (name,))
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
        self.cur.execute("SELECT acid,string_agg(codon, ' ') AS codons " +
                         "FROM codon_table " +
                         "WHERE name=(%s) " +
                         "GROUP BY acid " +
                         "ORDER BY acid;", (kind,))
        return self.cur.fetchall()
