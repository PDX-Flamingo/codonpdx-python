#!/usr/bin/env python

import ConfigParser
import time
import os
from db import dbManager


def clear(args):
    clearresultsdb(args)
    clearsharefiles(args)


def clearresultsdb(args):
    with dbManager('config/db.cfg') as db:
        db.clearResults(args.days)


def clearsharefiles(args):
    config = ConfigParser.RawConfigParser()
    config.read('config/codonpdx.cfg')
    path = config.get('share', 'path')
    for f in os.listdir(path):
        if (os.stat(os.path.join(path, f)).st_mtime <
                time.time() - args.days * 86400):
            os.remove(os.path.join(path, f))
