#!/usr/bin/env python

import json
import sys
from db import dbManager


# insert an organism into a database table
def insert(args):
    try:
        data = json.loads(args.json)
    except AttributeError:
        data = json.load(args.infile)
    with dbManager('config/db.cfg') as db:
        for org in data:
            db.insertOrganism(org, args.dbname, args.job)
    return data
