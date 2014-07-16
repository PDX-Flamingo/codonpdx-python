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
        count_input.infile = file
        count_input.format = format
        count_input.pretty = False
        count_input.output = json_file
        json = codonpdx.count.count(count_input)

    # put json into database
    with open(json_name, 'r') as json_file:
        insert_input = type('', (), {})
        insert_input.infile = json_file
        insert_input.dbname = 'input'
        input = codonpdx.insert.insert(insert_input)

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


# Test Methods
@app.task
def random_int(job):
    print "Start " + str(job)
    sleep(uniform(0, 2))
    return randint(1, 100)


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
