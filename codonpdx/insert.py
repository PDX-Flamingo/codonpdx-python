#!/usr/bin/env python

import json
import sys
from db import dbManager


# insert an organism into a database table
def insert(args):
    if hasattr(args, 'json'):
        data = json.loads(args.json)
    else:
        data = json.load(args.infile)
    with dbManager('config/db.cfg') as db:
        for org in data:
            db.insertOrganism(org, args.dbname, args.job)
    return data


# insert an organism into a database table
def insertinput(args):
    if hasattr(args, 'json'):
        data = json.loads(args.json)
    else:
        data = json.load(args.infile)
    with dbManager('config/db.cfg') as db:
        for org in data:
            db.insertInputOrganism(org, args.job)
    return data
