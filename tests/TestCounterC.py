""" Unit Tests for CounterC """

from ctypes import *
from CodonCountStruct import CodonCount
from nose.tools import ok_, eq_, istest


def getdict(struct):
    return dict(
        (field, getattr(struct, field)) for field, _ in struct._fields_
    )


class TestCounterC():
    counterc = CDLL('./counterc.so')
    counterc.countcodons.argtypes = (c_char_p,)
    counterc.countcodons.restype = CodonCount

    def __init__(self):
        self.data = []

    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    @istest
    def test_empty_sequence(self):
        countstruct = getdict(self.counterc.countcodons(""))
        for key in countstruct:
            eq_(countstruct[key], 0)

    @istest
    def test_not_a_sequence(self):
        countstruct = getdict(self.counterc.countcodons("Are you going to Scarborough Fair?"))
        for key in countstruct:
            eq_(countstruct[key], 0)

    @istest
    def test_simple_sequence_five_each(self):
        one_each = ("TTTTTCTTATTGTCTTCCTCATCGTATTACTAATAGTGTTGCTGATGGCTTCTCC"
                    "TACTGCCTCCCCCACCGCATCACCAACAGCGTCGCCGACGGATTATCATAATGAC"
                    "TACCACAACGAATAACAAAAAGAGTAGCAGAAGGGTTGTCGTAGTGGCTGCCGCA"
                    "GCGGATGACGAAGAGGGTGGCGGAGGGTTTTTCTTATTGTCTTCCTCATCGTATT"
                    "ACTAATAGTGTTGCTGATGGCTTCTCCTACTGCCTCCCCCACCGCATCACCAACA"
                    "GCGTCGCCGACGGATTATCATAATGACTACCACAACGAATAACAAAAAGAGTAGC"
                    "AGAAGGGTTGTCGTAGTGGCTGCCGCAGCGGATGACGAAGAGGGTGGCGGAGGGT"
                    "TTTTCTTATTGTCTTCCTCATCGTATTACTAATAGTGTTGCTGATGGCTTCTCCT"
                    "ACTGCCTCCCCCACCGCATCACCAACAGCGTCGCCGACGGATTATCATAATGACT"
                    "ACCACAACGAATAACAAAAAGAGTAGCAGAAGGGTTGTCGTAGTGGCTGCCGCAG"
                    "CGGATGACGAAGAGGGTGGCGGAGGGTTTTTCTTATTGTCTTCCTCATCGTATTA"
                    "CTAATAGTGTTGCTGATGGCTTCTCCTACTGCCTCCCCCACCGCATCACCAACAG"
                    "CGTCGCCGACGGATTATCATAATGACTACCACAACGAATAACAAAAAGAGTAGCA"
                    "GAAGGGTTGTCGTAGTGGCTGCCGCAGCGGATGACGAAGAGGGTGGCGGAGGGTT"
                    "TTTCTTATTGTCTTCCTCATCGTATTACTAATAGTGTTGCTGATGGCTTCTCCTA"
                    "CTGCCTCCCCCACCGCATCACCAACAGCGTCGCCGACGGATTATCATAATGACTA"
                    "CCACAACGAATAACAAAAAGAGTAGCAGAAGGGTTGTCGTAGTGGCTGCCGCAGC"
                    "GGATGACGAAGAGGGTGGCGGAGGG")
        countstruct = getdict(self.counterc.countcodons(one_each))
        for key in countstruct:
            eq_(countstruct[key], 5)

    @istest
    def test_simple_sequence_modulo_3_is_0(self):
        countstruct = getdict(self.counterc.countcodons("AAACCCTTTGGG"))
        eq_(countstruct['TTT'], 1)
        eq_(countstruct['TTC'], 0)
        eq_(countstruct['TTA'], 0)
        eq_(countstruct['TTG'], 0)
        eq_(countstruct['TCT'], 0)
        eq_(countstruct['TCC'], 0)
        eq_(countstruct['TCA'], 0)
        eq_(countstruct['TCG'], 0)
        eq_(countstruct['TAT'], 0)
        eq_(countstruct['TAC'], 0)
        eq_(countstruct['TAA'], 0)
        eq_(countstruct['TAG'], 0)
        eq_(countstruct['TGT'], 0)
        eq_(countstruct['TGC'], 0)
        eq_(countstruct['TGA'], 0)
        eq_(countstruct['TGG'], 0)
        eq_(countstruct['CTT'], 0)
        eq_(countstruct['CTC'], 0)
        eq_(countstruct['CTA'], 0)
        eq_(countstruct['CTG'], 0)
        eq_(countstruct['CCT'], 0)
        eq_(countstruct['CCC'], 1)
        eq_(countstruct['CCA'], 0)
        eq_(countstruct['CCG'], 0)
        eq_(countstruct['CAT'], 0)
        eq_(countstruct['CAC'], 0)
        eq_(countstruct['CAA'], 0)
        eq_(countstruct['CAG'], 0)
        eq_(countstruct['CGT'], 0)
        eq_(countstruct['CGC'], 0)
        eq_(countstruct['CGA'], 0)
        eq_(countstruct['CGG'], 0)
        eq_(countstruct['ATT'], 0)
        eq_(countstruct['ATC'], 0)
        eq_(countstruct['ATA'], 0)
        eq_(countstruct['ATG'], 0)
        eq_(countstruct['ACT'], 0)
        eq_(countstruct['ACC'], 0)
        eq_(countstruct['ACA'], 0)
        eq_(countstruct['ACG'], 0)
        eq_(countstruct['AAT'], 0)
        eq_(countstruct['AAC'], 0)
        eq_(countstruct['AAA'], 1)
        eq_(countstruct['AAG'], 0)
        eq_(countstruct['AGT'], 0)
        eq_(countstruct['AGC'], 0)
        eq_(countstruct['AGA'], 0)
        eq_(countstruct['AGG'], 0)
        eq_(countstruct['GTT'], 0)
        eq_(countstruct['GTC'], 0)
        eq_(countstruct['GTA'], 0)
        eq_(countstruct['GTG'], 0)
        eq_(countstruct['GCT'], 0)
        eq_(countstruct['GCC'], 0)
        eq_(countstruct['GCA'], 0)
        eq_(countstruct['GCG'], 0)
        eq_(countstruct['GAT'], 0)
        eq_(countstruct['GAC'], 0)
        eq_(countstruct['GAA'], 0)
        eq_(countstruct['GAG'], 0)
        eq_(countstruct['GGT'], 0)
        eq_(countstruct['GGC'], 0)
        eq_(countstruct['GGA'], 0)
        eq_(countstruct['GGG'], 1)

    @istest
    def test_simple_sequence_modulo_3_is_1(self):
        countstruct = getdict(self.counterc.countcodons("AAACCCTTTGGGA"))
        eq_(countstruct['TTT'], 1)
        eq_(countstruct['TTC'], 0)
        eq_(countstruct['TTA'], 0)
        eq_(countstruct['TTG'], 0)
        eq_(countstruct['TCT'], 0)
        eq_(countstruct['TCC'], 0)
        eq_(countstruct['TCA'], 0)
        eq_(countstruct['TCG'], 0)
        eq_(countstruct['TAT'], 0)
        eq_(countstruct['TAC'], 0)
        eq_(countstruct['TAA'], 0)
        eq_(countstruct['TAG'], 0)
        eq_(countstruct['TGT'], 0)
        eq_(countstruct['TGC'], 0)
        eq_(countstruct['TGA'], 0)
        eq_(countstruct['TGG'], 0)
        eq_(countstruct['CTT'], 0)
        eq_(countstruct['CTC'], 0)
        eq_(countstruct['CTA'], 0)
        eq_(countstruct['CTG'], 0)
        eq_(countstruct['CCT'], 0)
        eq_(countstruct['CCC'], 1)
        eq_(countstruct['CCA'], 0)
        eq_(countstruct['CCG'], 0)
        eq_(countstruct['CAT'], 0)
        eq_(countstruct['CAC'], 0)
        eq_(countstruct['CAA'], 0)
        eq_(countstruct['CAG'], 0)
        eq_(countstruct['CGT'], 0)
        eq_(countstruct['CGC'], 0)
        eq_(countstruct['CGA'], 0)
        eq_(countstruct['CGG'], 0)
        eq_(countstruct['ATT'], 0)
        eq_(countstruct['ATC'], 0)
        eq_(countstruct['ATA'], 0)
        eq_(countstruct['ATG'], 0)
        eq_(countstruct['ACT'], 0)
        eq_(countstruct['ACC'], 0)
        eq_(countstruct['ACA'], 0)
        eq_(countstruct['ACG'], 0)
        eq_(countstruct['AAT'], 0)
        eq_(countstruct['AAC'], 0)
        eq_(countstruct['AAA'], 1)
        eq_(countstruct['AAG'], 0)
        eq_(countstruct['AGT'], 0)
        eq_(countstruct['AGC'], 0)
        eq_(countstruct['AGA'], 0)
        eq_(countstruct['AGG'], 0)
        eq_(countstruct['GTT'], 0)
        eq_(countstruct['GTC'], 0)
        eq_(countstruct['GTA'], 0)
        eq_(countstruct['GTG'], 0)
        eq_(countstruct['GCT'], 0)
        eq_(countstruct['GCC'], 0)
        eq_(countstruct['GCA'], 0)
        eq_(countstruct['GCG'], 0)
        eq_(countstruct['GAT'], 0)
        eq_(countstruct['GAC'], 0)
        eq_(countstruct['GAA'], 0)
        eq_(countstruct['GAG'], 0)
        eq_(countstruct['GGT'], 0)
        eq_(countstruct['GGC'], 0)
        eq_(countstruct['GGA'], 0)
        eq_(countstruct['GGG'], 1)

    @istest
    def test_simple_sequence_modulo_3_is_2(self):
        countstruct = getdict(self.counterc.countcodons("AAACCCTTTGGGAC"))
        eq_(countstruct['TTT'], 1)
        eq_(countstruct['TTC'], 0)
        eq_(countstruct['TTA'], 0)
        eq_(countstruct['TTG'], 0)
        eq_(countstruct['TCT'], 0)
        eq_(countstruct['TCC'], 0)
        eq_(countstruct['TCA'], 0)
        eq_(countstruct['TCG'], 0)
        eq_(countstruct['TAT'], 0)
        eq_(countstruct['TAC'], 0)
        eq_(countstruct['TAA'], 0)
        eq_(countstruct['TAG'], 0)
        eq_(countstruct['TGT'], 0)
        eq_(countstruct['TGC'], 0)
        eq_(countstruct['TGA'], 0)
        eq_(countstruct['TGG'], 0)
        eq_(countstruct['CTT'], 0)
        eq_(countstruct['CTC'], 0)
        eq_(countstruct['CTA'], 0)
        eq_(countstruct['CTG'], 0)
        eq_(countstruct['CCT'], 0)
        eq_(countstruct['CCC'], 1)
        eq_(countstruct['CCA'], 0)
        eq_(countstruct['CCG'], 0)
        eq_(countstruct['CAT'], 0)
        eq_(countstruct['CAC'], 0)
        eq_(countstruct['CAA'], 0)
        eq_(countstruct['CAG'], 0)
        eq_(countstruct['CGT'], 0)
        eq_(countstruct['CGC'], 0)
        eq_(countstruct['CGA'], 0)
        eq_(countstruct['CGG'], 0)
        eq_(countstruct['ATT'], 0)
        eq_(countstruct['ATC'], 0)
        eq_(countstruct['ATA'], 0)
        eq_(countstruct['ATG'], 0)
        eq_(countstruct['ACT'], 0)
        eq_(countstruct['ACC'], 0)
        eq_(countstruct['ACA'], 0)
        eq_(countstruct['ACG'], 0)
        eq_(countstruct['AAT'], 0)
        eq_(countstruct['AAC'], 0)
        eq_(countstruct['AAA'], 1)
        eq_(countstruct['AAG'], 0)
        eq_(countstruct['AGT'], 0)
        eq_(countstruct['AGC'], 0)
        eq_(countstruct['AGA'], 0)
        eq_(countstruct['AGG'], 0)
        eq_(countstruct['GTT'], 0)
        eq_(countstruct['GTC'], 0)
        eq_(countstruct['GTA'], 0)
        eq_(countstruct['GTG'], 0)
        eq_(countstruct['GCT'], 0)
        eq_(countstruct['GCC'], 0)
        eq_(countstruct['GCA'], 0)
        eq_(countstruct['GCG'], 0)
        eq_(countstruct['GAT'], 0)
        eq_(countstruct['GAC'], 0)
        eq_(countstruct['GAA'], 0)
        eq_(countstruct['GAG'], 0)
        eq_(countstruct['GGT'], 0)
        eq_(countstruct['GGC'], 0)
        eq_(countstruct['GGA'], 0)
        eq_(countstruct['GGG'], 1)

    @istest
    def test_simple_sequence_invalid_in_the_middle(self):
        countstruct = getdict(self.counterc.countcodons("AAACCCTNTNTNNAATTTGGG"))
        eq_(countstruct['TTT'], 1)
        eq_(countstruct['TTC'], 0)
        eq_(countstruct['TTA'], 0)
        eq_(countstruct['TTG'], 0)
        eq_(countstruct['TCT'], 0)
        eq_(countstruct['TCC'], 0)
        eq_(countstruct['TCA'], 0)
        eq_(countstruct['TCG'], 0)
        eq_(countstruct['TAT'], 0)
        eq_(countstruct['TAC'], 0)
        eq_(countstruct['TAA'], 0)
        eq_(countstruct['TAG'], 0)
        eq_(countstruct['TGT'], 0)
        eq_(countstruct['TGC'], 0)
        eq_(countstruct['TGA'], 0)
        eq_(countstruct['TGG'], 0)
        eq_(countstruct['CTT'], 0)
        eq_(countstruct['CTC'], 0)
        eq_(countstruct['CTA'], 0)
        eq_(countstruct['CTG'], 0)
        eq_(countstruct['CCT'], 0)
        eq_(countstruct['CCC'], 1)
        eq_(countstruct['CCA'], 0)
        eq_(countstruct['CCG'], 0)
        eq_(countstruct['CAT'], 0)
        eq_(countstruct['CAC'], 0)
        eq_(countstruct['CAA'], 0)
        eq_(countstruct['CAG'], 0)
        eq_(countstruct['CGT'], 0)
        eq_(countstruct['CGC'], 0)
        eq_(countstruct['CGA'], 0)
        eq_(countstruct['CGG'], 0)
        eq_(countstruct['ATT'], 0)
        eq_(countstruct['ATC'], 0)
        eq_(countstruct['ATA'], 0)
        eq_(countstruct['ATG'], 0)
        eq_(countstruct['ACT'], 0)
        eq_(countstruct['ACC'], 0)
        eq_(countstruct['ACA'], 0)
        eq_(countstruct['ACG'], 0)
        eq_(countstruct['AAT'], 0)
        eq_(countstruct['AAC'], 0)
        eq_(countstruct['AAA'], 1)
        eq_(countstruct['AAG'], 0)
        eq_(countstruct['AGT'], 0)
        eq_(countstruct['AGC'], 0)
        eq_(countstruct['AGA'], 0)
        eq_(countstruct['AGG'], 0)
        eq_(countstruct['GTT'], 0)
        eq_(countstruct['GTC'], 0)
        eq_(countstruct['GTA'], 0)
        eq_(countstruct['GTG'], 0)
        eq_(countstruct['GCT'], 0)
        eq_(countstruct['GCC'], 0)
        eq_(countstruct['GCA'], 0)
        eq_(countstruct['GCG'], 0)
        eq_(countstruct['GAT'], 0)
        eq_(countstruct['GAC'], 0)
        eq_(countstruct['GAA'], 0)
        eq_(countstruct['GAG'], 0)
        eq_(countstruct['GGT'], 0)
        eq_(countstruct['GGC'], 0)
        eq_(countstruct['GGA'], 0)
        eq_(countstruct['GGG'], 1)

    @istest
    def test_random_sequence(self):
        term1_seq = ("ACCAGCGCACTTCGGCAGCGGCAGCACCTCGGCAGCGTC"
                     "AGTGAAAATGCCAAGCAAGAAAAGCGGCCCGCAACCCCA"
                     "TAAGAGGTGGGTGTTCACCCTTAATAATCCTTCCGAGGA"
                     "GGAGAAAAACAAAATACGGGAGCTTCCAATCTCCCTTTT"
                     "TGATTATTTTGTTTGCGGAGAGGAAGGTTTGGAAGAGGG"
                     "TAGAACTCCTCACCTCCAGGGGTTTGCGAATTTTGCTAA"
                     "GAAGCAGACTTTTAACAAGGTGAAGTGGTATTTTGGTGC"
                     "CCGCTGCCACATCGAGAAAGCGAAAGGAACCGACCAGCA"
                     "GAATAAAGAATACTGCAGTAAAGAAGGCCACATACTTAT"
                     "CGAGTGTGGAGCTCCGCGGAACCAGGGGAAGCGCAGCGA"
                     "CCTGTCTACTGCTGTGAGTACCCTTTTGGAGACGGGGTC"
                     "TTTGGTGACTGTAGCCGAGCAGTTCCCTGTAACGTATGT"
                     "GAGAAATTTCCGCGGGCTGGCTGAACTTTTGAAAGTGAG"
                     "CGGGAAGATGCAGCAGCGTGATTGGAAGACAGCTGTACA"
                     "CGTCATAGTGGGCCCGCCCGGTTGTGGGAAGAGCCAGTG"
                     "GGCCCGTAATTTTGCTGAGCCTAGCGACACCTACTGGAA"
                     "GCCTAGTAGAAATAAGTGGTGGGATGGATATCATGGAGA"
                     "AGAAGTTGTTGTTTTGGATGATTTTTATGGCTGGTTACC"
                     "TTGGGATGATCTACTGAGACTGTGTGACCGGTATCCATT"
                     "GACTGTAGAGACTAAAGGCGGTACTGTTCCTTTTTTGGC"
                     "CCGCAGTATTTTGATTACCAGCAATCAGGCCCCCCAGGA"
                     "ATGGTACTCCTCAACTGCTGTCCCAGCTGTAGAAGCTCT"
                     "CTATCGGAGGATTACTACTTTGCAATTTTGGAAGACTGC"
                     "TGGAGAACAATCCACGGAGGTACCCGAAGGCCGATTTGA"
                     "AGCAGTGGACCCACCCTGTGCCCTTTTCCCATATAAAAT"
                     "AAATTACTGAGTCTTTTTTGTTATCACATCGTAATGGTT"
                     "TTTATTTTTATTTATTTAGAGGGTCTTTTAGGATAAATT"
                     "CTCTGAATTGTACATAAATAGTCAGCCTTACCACATAAT"
                     "TTTGGGCTGTGGCTGCATTTTGGAGCGCATAGCCGAGGC"
                     "CTGTGTGCTCGACATTGGTGTGGGTATTTAAATGGAGCC"
                     "ACAGCTGGTTTCTTTTATTATTTGGTTGGAACCAATCAA"
                     "TTGTTTGGTCCAGCTCAGGTTTGGGGGTGAAGTACCTGG"
                     "AGTGGTAGGTAAAGGGCTGCCTTATGGTGTGGCGGGAGG"
                     "AGTAGTTAATATAGGGGTCATAGGCCAAGTTGGTGGAGG"
                     "GGGTTACAAAGTTGGCATCCAAGATAACAACAGTGGACC"
                     "CAACACCTCTTTCATTAGAGGTGATGGGGTCTCTGGGGT"
                     "AAAATTCATATTTAGCCTTTCTAATACGGTAGTATTGGA"
                     "AAGGTAGGGGTAGGGGGTTGGTGCCGCCTGAGGGGGGGA"
                     "GGAACTGGCCGATGTTGAATTTGAGGTGGTTAACATGCC"
                     "AAGATGGCTGCGAGTATCCTCCTTTTATGGTGAGTACAA"
                     "ATTCTGTAGAAAGGCGGGAATTGAAGATACCCGTCTTTC"
                     "GGCGCCATCTGTAACGGTTTCTGAAGGCGGGGTGTGCCA"
                     "AATATGGTCTTCTCCGGAGGATGTTTCCAAGATGGCTGC"
                     "GGGGGCGGGTCCTTCGTCTGCGGTAACGCCTCCTTGGCC"
                     "ACGTCATCCTATAAAAGTGAAAGAAGTGCGCTGCTGTAG"
                     "TATT"
        )
        countstruct = getdict(self.counterc.countcodons(term1_seq))
        eq_(countstruct['TTT'], 26)
        eq_(countstruct['TTC'], 8)
        eq_(countstruct['TTA'], 10)
        eq_(countstruct['TTG'], 8)
        eq_(countstruct['TCT'], 3)
        eq_(countstruct['TCC'], 10)
        eq_(countstruct['TCA'], 5)
        eq_(countstruct['TCG'], 1)
        eq_(countstruct['TAT'], 10)
        eq_(countstruct['TAC'], 8)
        eq_(countstruct['TAA'], 17)
        eq_(countstruct['TAG'], 9)
        eq_(countstruct['TGT'], 19)
        eq_(countstruct['TGC'], 11)
        eq_(countstruct['TGA'], 16)
        eq_(countstruct['TGG'], 20)
        eq_(countstruct['CTT'], 4)
        eq_(countstruct['CTC'], 8)
        eq_(countstruct['CTA'], 2)
        eq_(countstruct['CTG'], 13)
        eq_(countstruct['CCT'], 7)
        eq_(countstruct['CCC'], 7)
        eq_(countstruct['CCA'], 13)
        eq_(countstruct['CCG'], 7)
        eq_(countstruct['CAT'], 13)
        eq_(countstruct['CAC'], 6)
        eq_(countstruct['CAA'], 10)
        eq_(countstruct['CAG'], 8)
        eq_(countstruct['CGT'], 1)
        eq_(countstruct['CGC'], 1)
        eq_(countstruct['CGA'], 11)
        eq_(countstruct['CGG'], 9)
        eq_(countstruct['ATT'], 12)
        eq_(countstruct['ATC'], 4)
        eq_(countstruct['ATA'], 3)
        eq_(countstruct['ATG'], 4)
        eq_(countstruct['ACT'], 5)
        eq_(countstruct['ACC'], 8)
        eq_(countstruct['ACA'], 3)
        eq_(countstruct['ACG'], 2)
        eq_(countstruct['AAT'], 9)
        eq_(countstruct['AAC'], 6)
        eq_(countstruct['AAA'], 8)
        eq_(countstruct['AAG'], 4)
        eq_(countstruct['AGT'], 16)
        eq_(countstruct['AGC'], 10)
        eq_(countstruct['AGA'], 12)
        eq_(countstruct['AGG'], 14)
        eq_(countstruct['GTT'], 7)
        eq_(countstruct['GTC'], 5)
        eq_(countstruct['GTA'], 9)
        eq_(countstruct['GTG'], 8)
        eq_(countstruct['GCT'], 7)
        eq_(countstruct['GCC'], 11)
        eq_(countstruct['GCA'], 8)
        eq_(countstruct['GCG'], 6)
        eq_(countstruct['GAT'], 4)
        eq_(countstruct['GAC'], 7)
        eq_(countstruct['GAA'], 18)
        eq_(countstruct['GAG'], 8)
        eq_(countstruct['GGT'], 18)
        eq_(countstruct['GGC'], 12)
        eq_(countstruct['GGA'], 21)
        eq_(countstruct['GGG'], 16)

    @istest
    def test_random_sequence(self):
        f = open('cow.seq', 'r')
        countstruct = getdict(self.counterc.countcodons(f.readline()))
        eq_(countstruct['TTT'], 1169127)
        eq_(countstruct['TTC'], 572415)
        eq_(countstruct['TTA'], 653679)
        eq_(countstruct['TTG'], 551344)
        eq_(countstruct['TCT'], 628490)
        eq_(countstruct['TCC'], 402091)
        eq_(countstruct['TCA'], 557273)
        eq_(countstruct['TCG'], 52363)
        eq_(countstruct['TAT'], 647698)
        eq_(countstruct['TAC'], 338345)
        eq_(countstruct['TAA'], 650744)
        eq_(countstruct['TAG'], 385361)
        eq_(countstruct['TGT'], 574118)
        eq_(countstruct['TGC'], 381261)
        eq_(countstruct['TGA'], 556172)
        eq_(countstruct['TGG'], 479804)
        eq_(countstruct['CTT'], 578526)
        eq_(countstruct['CTC'], 432919)
        eq_(countstruct['CTA'], 383136)
        eq_(countstruct['CTG'], 521121)
        eq_(countstruct['CCT'], 455130)
        eq_(countstruct['CCC'], 310692)
        eq_(countstruct['CCA'], 478747)
        eq_(countstruct['CCG'], 58156)
        eq_(countstruct['CAT'], 531415)
        eq_(countstruct['CAC'], 387600)
        eq_(countstruct['CAA'], 546849)
        eq_(countstruct['CAG'], 520075)
        eq_(countstruct['CGT'], 59720)
        eq_(countstruct['CGC'], 50561)
        eq_(countstruct['CGA'], 52125)
        eq_(countstruct['CGG'], 57943)
        eq_(countstruct['ATT'], 773553)
        eq_(countstruct['ATC'], 382642)
        eq_(countstruct['ATA'], 646304)
        eq_(countstruct['ATG'], 531010)
        eq_(countstruct['ACT'], 463769)
        eq_(countstruct['ACC'], 306416)
        eq_(countstruct['ACA'], 570762)
        eq_(countstruct['ACG'], 59782)
        eq_(countstruct['AAT'], 770510)
        eq_(countstruct['AAC'], 422809)
        eq_(countstruct['AAA'], 1160703)
        eq_(countstruct['AAG'], 577313)
        eq_(countstruct['AGT'], 463957)
        eq_(countstruct['AGC'], 365433)
        eq_(countstruct['AGA'], 627866)
        eq_(countstruct['AGG'], 458186)
        eq_(countstruct['GTT'], 426786)
        eq_(countstruct['GTC'], 251551)
        eq_(countstruct['GTA'], 339118)
        eq_(countstruct['GTG'], 389988)
        eq_(countstruct['GCT'], 365314)
        eq_(countstruct['GCC'], 284110)
        eq_(countstruct['GCA'], 380165)
        eq_(countstruct['GCG'], 50561)
        eq_(countstruct['GAT'], 382211)
        eq_(countstruct['GAC'], 249625)
        eq_(countstruct['GAA'], 571097)
        eq_(countstruct['GAG'], 434060)
        eq_(countstruct['GGT'], 306196)
        eq_(countstruct['GGC'], 285218)
        eq_(countstruct['GGA'], 403467)
        eq_(countstruct['GGG'], 310647)
