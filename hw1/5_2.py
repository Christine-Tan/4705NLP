#! /usr/bin/python3

__author__ = "Xinyue Tan <xt2215"
__date__ = "$Sep 17, 2018"

import sys
import viterbi as v
import os

def usage():
    sys.stderr.write("""
    Usage: python 5_2.py ner_dev.dat > 5_2.txt
        using the Viterbi to estimate tagger with the extra log likelihood column
        write the result into 5_2.txt\n""")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.argv.append("ner_dev.dat")
    elif len(sys.argv) != 2:
        # Expect exactly one argument: the test data file.
        usage();
        sys.exit(2)

    try:
        test_file = open(sys.argv[1], "r");
        ner_key_file = open("5_2.txt","w+");
        v.viterbi(test_file, ner_key_file);
    except IOError:
        sys.stderr.write("ERROR: Cannot read input file %s or %s.\n" % sys.argv[1]);
        sys.exit(1)
