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

Dependencies
-----
* [BioPython](http://biopython.org) 

Usage
-------

### Mirror
```bash
./codonpdx.py mirror -d refseq
```

### Count

generate codon count metadata for a file

```bash
zcat ~/refseq/release/complete/complete.1.genomic.gbff.gz| ./codonpdx.py count -f genbank > /tmp/complete.1.json
```

### LoadDB

load count metadata into refseq

```bash
cat /tmp/complete.1.json | ./codonpdx.py loadDB -d refseq
```

### calcScore

calculate scores for NG_027788.1

```bash
./codonpdx.py calcScore -d refseq -v NG_027788.1
```

### Celery

Run as celery worker process

```bash
celery -A codonpdx worker -l info
```

Results
--------

| *DataSet* | *Version* | *OS* | *Compiler* | *Python* | *codonpdx* | *Jobs* | *Time* | 
|-----------|-----------|------|------------|----------|------------|--------|--------|
| refseq  | Release 65 | CentOS 6 | GCC 4.9.0 | PyPy 2.31 | v1.0.0 | 32 | 12.35 minutes |
| genbank | Release 201 | CentOS 6 | GCC 4.9.0 | PyPy 2.31 | v1.0.0| 32 | 95.20 minutes |
