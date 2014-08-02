codonpdx-python
===============

[![Build Status](https://travis-ci.org/PDX-Flamingo/codonpdx-python.svg?branch=master)](https://travis-ci.org/PDX-Flamingo/codonpdx-python)

Python version of the codonpdx counter

Setup
-----

Create a PyPy virtualenv and then run the following commands.

```bash
source .venv/bin/activate
pip install -r requirements.txt
make
```

Configuration
-------------

There are several configuration files that need to be configured before use.

Sample configuration files are provided for the following:

config/db.cfg
config/mirror.cfg
config/codonpdx.cfg
codonpdx/celeryconfig.py

Usage
-------

### Mirror

Mirror refseq or genbank to local disk.

```bash
./codonpdx.py mirror -d refseq
```

### queueJobs

One or more celery workers must be running before running this. This command
will count codon count data and insert it into to the database.

```bash
./codonpdx queueJobs -d {refseq,genbank} -f {fasta,genbank}
```

### Count

generate codon count metadata for a file

```bash
zcat ~/refseq/release/complete/complete.1.genomic.gbff.gz| ./codonpdx.py count -f genbank > /tmp/complete.1.json
```

### Insert

load count metadata into refseq

```bash
cat /tmp/complete.1.json | ./codonpdx.py insert -d refseq
```

### Calc

calculate scores for NG_027788.1

```bash
./codonpdx.py calc -d refseq -v NG_027788.1
```

### Starting a celery worker

This will start a celery worker which is used by the webapp and mirror command.

```bash
celery -A codonpdx worker -l info
```

Results
--------

| *DataSet* | *Version* | *OS* | *Compiler* | *Python* | *codonpdx* | *Jobs* | *Time* | 
|-----------|-----------|------|------------|----------|------------|--------|--------|
| refseq  | Release 65 | CentOS 6 | GCC 4.9.0 | PyPy 2.31 | v1.0.0 | 32 | 12.35 minutes |
| genbank | Release 201 | CentOS 6 | GCC 4.9.0 | PyPy 2.31 | v1.0.0| 32 | 95.20 minutes |
