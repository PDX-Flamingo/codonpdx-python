from __future__ import absolute_import

import codonpdx.count
import codonpdx.insert
import codonpdx.calc

from time import sleep
from codonpdx.celery import app
from random import randint, uniform


### CodonPDX TASK Methods ###
@app.task
def trigger_demo_behavior(job, file):
	print "Demo Time!"
	return job

### Test Methods ###
@app.task
def random_int(job):
	print "Start " + str(job)
	sleep(uniform(0,2))
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