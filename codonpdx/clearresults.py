#!/usr/bin/env python

from db import dbManager


def clear(args):
    with dbManager('config/db.cfg') as db:
        db.clearResults()
