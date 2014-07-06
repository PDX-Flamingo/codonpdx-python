import codonpdx.count
import getopt
import sys


def main(argv):
    inputfile = sys.stdin
    format = 'fasta'
    prettyPrint = False
    try:
        opts, args = getopt.getopt(argv, "hi:f:p",
                                   ["ifile=", "format=", "pretty"])
    except getopt.GetoptError:
        print ('count.py -i <inputfile> -f <format>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('count.py -i <inputfile> -f <format>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-f", "--format"):
            format = arg
        elif opt in ("-p", "--pretty"):
            prettyPrint = True

    codonpdx.count.codonCount(inputfile, format, prettyPrint)


if __name__ == "__main__":
    main(sys.argv[1:])
