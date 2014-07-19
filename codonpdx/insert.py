#!/usr/bin/env python

import json
import sys
from db import dbManager


# insert an organism into a database table
def insert(args):
    data = json.load(args.infile)
    with dbManager('config/db.cfg') as db:
        for org in data:
            db.insertOrganism(org, args.dbname)
    return data
