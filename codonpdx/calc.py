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
		self.cur.execute("SELECT * FROM "+source+";");
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

# compare a virus to organisms in a sequence database
# db: the database manager used to get the data from
# virus_name: the accession and version number of the virus
# seq_db: the name of the sequence database table
# codon_table_name: the name of the codon table
def comparison(db, virus_name, seq_db, codon_table_name='standard'):
	virus = db.getOrganism(virus_name, seq_db)
	codon_table = db.getCodonTable(codon_table_name)
	scores = defaultdict(int)
	virus_ratio = ratio(virus, codon_table)
	for organism in db.getOrganisms(seq_db):
		organism_ratio = ratio(organism, codon_table)
		# calculate the score for the virus and this organism
		for k in virus_ratio:
			scores[organism['id']] += abs(virus_ratio[k] - organism_ratio[k])
	return scores
	
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
			codon_total = int(organism[codon.lower()])
			if(codon_total != 0):
				ratio = codon_total / acid_total
			else:
				ratio = 0
			# store ratio for this codon
			ratios[codon] = ratio
	return ratios

def calcScore(args):
	db = dbManager('config/db.cfg')
	# do a comparison of virus 'NG_027788.1' with codon table 'standard'
	results = comparison(db, args.virus, args.dbname, 'standard')
	for k in sorted(results, key=results.get):
		print results[k], k
