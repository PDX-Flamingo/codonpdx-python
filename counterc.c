#include "counterc.h"

CodonCount countcodons(char * sequence)
{
    char codon[4];
    long seq_length = strlen(sequence) - 2;
    const char * valid_characters = "ACTG";
    char * c = codon;

    Trie * codoncount = trie_new();     // You create it, you destroy it

    for (int i = 0; i < seq_length; i+=3)
    {
        int invalid = 0;

        strncpy(codon, sequence+i, 3);
        codon[3] = '\0';                // Ensure codon ends at 3 characters

        // Break out if invalid character detected
        while (*c) {
            if (!strchr(valid_characters, *c)) {
                invalid = 1;
                break;
            }
            c++;
        }

        if (invalid == 1) { continue; }

        trie_increment(codoncount, codon);
    }

    // Prepare struct to return
    // Trie is not an iterable structure, thus the length
    struct CodonCount counts;
    counts.TTT = (long long) trie_lookup(codoncount, "TTT");
    counts.TTC = (long long) trie_lookup(codoncount, "TTC");
    counts.TTA = (long long) trie_lookup(codoncount, "TTA");
    counts.TTG = (long long) trie_lookup(codoncount, "TTG");
    counts.TCT = (long long) trie_lookup(codoncount, "TCT");
    counts.TCC = (long long) trie_lookup(codoncount, "TCC");
    counts.TCA = (long long) trie_lookup(codoncount, "TCA");
    counts.TCG = (long long) trie_lookup(codoncount, "TCG");
    counts.TAT = (long long) trie_lookup(codoncount, "TAT");
    counts.TAC = (long long) trie_lookup(codoncount, "TAC");
    counts.TAA = (long long) trie_lookup(codoncount, "TAA");
    counts.TAG = (long long) trie_lookup(codoncount, "TAG");
    counts.TGT = (long long) trie_lookup(codoncount, "TGT");
    counts.TGC = (long long) trie_lookup(codoncount, "TGC");
    counts.TGA = (long long) trie_lookup(codoncount, "TGA");
    counts.TGG = (long long) trie_lookup(codoncount, "TGG");
    counts.CTT = (long long) trie_lookup(codoncount, "CTT");
    counts.CTC = (long long) trie_lookup(codoncount, "CTC");
    counts.CTA = (long long) trie_lookup(codoncount, "CTA");
    counts.CTG = (long long) trie_lookup(codoncount, "CTG");
    counts.CCT = (long long) trie_lookup(codoncount, "CCT");
    counts.CCC = (long long) trie_lookup(codoncount, "CCC");
    counts.CCA = (long long) trie_lookup(codoncount, "CCA");
    counts.CCG = (long long) trie_lookup(codoncount, "CCG");
    counts.CAT = (long long) trie_lookup(codoncount, "CAT");
    counts.CAC = (long long) trie_lookup(codoncount, "CAC");
    counts.CAA = (long long) trie_lookup(codoncount, "CAA");
    counts.CAG = (long long) trie_lookup(codoncount, "CAG");
    counts.CGT = (long long) trie_lookup(codoncount, "CGT");
    counts.CGC = (long long) trie_lookup(codoncount, "CGC");
    counts.CGA = (long long) trie_lookup(codoncount, "CGA");
    counts.CGG = (long long) trie_lookup(codoncount, "CGG");
    counts.ATT = (long long) trie_lookup(codoncount, "ATT");
    counts.ATC = (long long) trie_lookup(codoncount, "ATC");
    counts.ATA = (long long) trie_lookup(codoncount, "ATA");
    counts.ATG = (long long) trie_lookup(codoncount, "ATG");
    counts.ACT = (long long) trie_lookup(codoncount, "ACT");
    counts.ACC = (long long) trie_lookup(codoncount, "ACC");
    counts.ACA = (long long) trie_lookup(codoncount, "ACA");
    counts.ACG = (long long) trie_lookup(codoncount, "ACG");
    counts.AAT = (long long) trie_lookup(codoncount, "AAT");
    counts.AAC = (long long) trie_lookup(codoncount, "AAC");
    counts.AAA = (long long) trie_lookup(codoncount, "AAA");
    counts.AAG = (long long) trie_lookup(codoncount, "AAG");
    counts.AGT = (long long) trie_lookup(codoncount, "AGT");
    counts.AGC = (long long) trie_lookup(codoncount, "AGC");
    counts.AGA = (long long) trie_lookup(codoncount, "AGA");
    counts.AGG = (long long) trie_lookup(codoncount, "AGG");
    counts.GTT = (long long) trie_lookup(codoncount, "GTT");
    counts.GTC = (long long) trie_lookup(codoncount, "GTC");
    counts.GTA = (long long) trie_lookup(codoncount, "GTA");
    counts.GTG = (long long) trie_lookup(codoncount, "GTG");
    counts.GCT = (long long) trie_lookup(codoncount, "GCT");
    counts.GCC = (long long) trie_lookup(codoncount, "GCC");
    counts.GCA = (long long) trie_lookup(codoncount, "GCA");
    counts.GCG = (long long) trie_lookup(codoncount, "GCG");
    counts.GAT = (long long) trie_lookup(codoncount, "GAT");
    counts.GAC = (long long) trie_lookup(codoncount, "GAC");
    counts.GAA = (long long) trie_lookup(codoncount, "GAA");
    counts.GAG = (long long) trie_lookup(codoncount, "GAG");
    counts.GGT = (long long) trie_lookup(codoncount, "GGT");
    counts.GGC = (long long) trie_lookup(codoncount, "GGC");
    counts.GGA = (long long) trie_lookup(codoncount, "GGA");
    counts.GGG = (long long) trie_lookup(codoncount, "GGG");

    trie_free(codoncount);

    return counts;
}