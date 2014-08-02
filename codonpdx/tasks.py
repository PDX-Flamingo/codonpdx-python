from __future__ import absolute_import

import codonpdx.count
import codonpdx.insert
import codonpdx.calc

from time import sleep
from codonpdx.celery import app
from random import randint, uniform


# CodonPDX TASK Methods
@app.task
def trigger_demo_behavior(job, file, seqdb, format):
    json_name = '/tmp/codonpdx_' + job + '.json'

    # first count the codons in the file
    with open(json_name, 'w+') as json_file:
        count_input = type('', (), {})
        count_input.job = job
        count_input.infile = file
        count_input.format = format
        count_input.pretty = False
        count_input.gzip = False
        count_input.output = json_file
        count_input.shuffle = True
        codonpdx.count.count(count_input)

    # put json into database
    with open(json_name, 'r') as json_file:
        insert_input = type('', (), {})
        insert_input.json = ""
        insert_input.infile = json_file
        insert_input.dbname = 'input'
        insert_input.job = job
        input = codonpdx.insert.insertinput(insert_input)

    # do comparison and place into results table
    calc_input = type('', (), {})
    # use the first sequence in the file
    calc_input.virus = input[0]['id']
    calc_input.virusdb = 'input'
    calc_input.output = False
    calc_input.job = job
    calc_input.dbname = seqdb
    codonpdx.calc.calc(calc_input)

    return job


@app.task
def parse_file(file, format, dbname):
    """Task to count codons and load them into the db"""

    parse_args = type('', (), {})
    parse_args.infile = file
    parse_args.output = False
    parse_args.format = format
    parse_args.dbname = dbname
    parse_args.gzip = True
    parse_args.pretty = False
    parse_args.job = None
    parse_args.json = codonpdx.count.count(parse_args)

    # If the file has sequences insert them
    if parse_args.json:
        codonpdx.insert.insert(parse_args)

    return file


# Simple task to check if calls are working
@app.task
def health_check():
    return True
