import ConfigParser
import glob
import os

from codonpdx.tasks import parse_file


def queueJobs(args):
    config = ConfigParser.RawConfigParser()
    config.read('config/codonpdx.cfg')
    path = config.get(args.dbname, 'path')
    pattern = config.get(args.dbname, 'pattern')
    files = [f for f in glob.glob(path + pattern) if os.path.isfile(f)]
    for file in files:
        parse_file.delay(file, args.format, args.dbname)
