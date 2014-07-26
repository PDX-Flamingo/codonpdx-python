import ConfigParser
import os


def mirror(args):
    config = ConfigParser.RawConfigParser()
    config.read('config/mirror.cfg')
    local = config.get(args.dbname, 'local')
    remote = config.get(args.dbname, 'remote')
    opts = '--delete --parallel=6'
    cmd = "/usr/bin/lftp -c 'connect {remote} && mirror {opts} . {local}'" \
        .format(**locals())
    print "Running " + cmd + "\n"
    os.system(cmd)
