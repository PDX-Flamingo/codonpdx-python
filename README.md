codonpdx-python
===============

[![Build Status](https://travis-ci.org/PDX-Flamingo/codonpdx-python.svg?branch=master)](https://travis-ci.org/PDX-Flamingo/codonpdx-python)

Python version of the codonpdx counter

Setup
-----

Create a virtualenv and then run the following commands.

```bash
pip install -r requirements.txt
make
```

C dependencies
-----

1. [C-Algorithms 1.2.0](http://c-algorithms.sourceforge.net)

Usage
-------

```bash
python main.py -i cow.rna.fna  > /tmp/output.json
```

Results
--------

| *DataSet* | *Version* | *OS* | *Compiler* | *Python* | *codonpdx* | *Time* | 
|-----------|-----------|------|------------|----------|----------|--------|
| refseq  | Release 65 | Centos 6 | GCC 4.9.0 | pypy 2.31 | v1.0.0 |  12.35 seconds |
