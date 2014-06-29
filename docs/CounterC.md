## CounterC
by Phil Tseng

### What Does It Do
From a sequence of DNA with the alphabet of {A,C,G,T}, return an object with the frequency counts of the 64 possible 3-letter codons, with the following constraints:

1. When an invalid character is encountered in a particular 3-letter codon, it is ignored and not counted.
2. When a codon is ignored, alignment of the original sequence is preserved by ignoring the current codon and moving on to the next codon.

### Why C?
Prototypes of this counter varied greatly in processing performance.  The following chart shows the processing time for a sample sequence of ~81 Million base pairs:

|  Prototype        |  Processing Time (ms) |
|-------------------|:---------------------:|
|  Python First Try |  ~60000               |
|  Python Optimized |  ~38000               |
|  Pypy Optimized   |  ~12000               |
|  Java First Try   |  ~5000                |
|  Pypy+C Optimized |   565					|
|  C optimized      |   364                 |

Because we will be processing more than 1 Trillion base pairs, it is critical that we achieve a high level of optimization.  C is helpful in this respect as it provides access to pointer arithmetic with a minimum amount of processing overhead.

### Why Python?
Prototypes of this counter attempted to use a [Genbank/Fasta parsing library based in C](http://www.biomedcentral.com/1471-2105/9/321).  While it was fast, it was not stable and would crash on parsing Genbank files with a long feature entry.  The developer has not updated this library since 2008.  Genbank/Fasta parsing can not be implemented in C.

The alternative is to call this C-based counter from Python, and use [BioPython](http://biopython.org) for parsing.  BioPython has a large and active community, and is actively being developed.  

### Why Pypy?
BioPython parsing of Genbank is notoriously slow.  We can achieve additional speedups by using the `pypy` implementation of Python, which provides a Just-In-Time compiler for Python code.  By switching to `pypy` we found that the parsing speed was approximately twice as fast.

### How the Counter Works
The following optimizations were utilized:

1. Operations were done in place as the sequence is being read.  Earlier implementations relied on the entire sequence being read first then processed after.  This counter does everything on one pass of the input sequence.  The codon is staged in a cache-friendly way, operated on, then overwritten by the following operation.

2. Filtering of invalid characters is done at the same time.  Earlier implementations counted codons with invalid characters and filtered after the entire sequence was read.  Here, filtering is done in place.  As soon as an invalid character is encountered, the loop short-circuits and moves on to the next codon.  The invalid codon is never counted.

3. Use of a "trie" (Radix tree) data structure.  Earlier implementations used hash tables.  With a trie, the codon sequence itself provides the address by which count values may be accessed.  Since the maximum length of each codon is three characters, use of a trie provides exactly O(3) performance for accessing and changing the count value.  No string comparison operation is ever used.  Because there are only 64 codon possibilities, this particular trie does not take up much space in memory, making the operation cache-friendly.  The trie implementation from [C-Algorithms](http://c-algorithms.sourceforge.net) was used.  It was modified to include a method for incrementing a codon count in one pass.  

### Future Improvements

This implementation of the C counter is currently implemented in `ctypes`.  Implementing in `cffi` may yield additional performance in `pypy`.