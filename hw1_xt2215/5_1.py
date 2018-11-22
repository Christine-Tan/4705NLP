#! /usr/bin/python3

__author__ = "Xinyue Tan <xt2215"
__date__ = "$Sep 17, 2018"

import math
import sys
import compute_log_q as logq
import os

"""
reads in lines of trigrams.txt (yi-2 yi-1 yi)
produces the file containing trigrams and their respective parameters in the format
 wi−2 wi−1 wi log q(wi|wi−2,wi−1) base on e
write the results into 5_1.txt
"""


def compute_trigram_q(count_file, trigram_file, trigram_q_file):
    bigram_count_dict, trigram_count_dict = logq.trigram_and_bigram_count(count_file);
    l = trigram_file.readline();
    while l:
        trigrams = l.strip().split(" ");
        trigram = (trigrams[0], trigrams[1], trigrams[2]);
        bigram = (trigrams[0], trigrams[1]);
        trigram_count = trigram_count_dict.get(trigram, 0);
        bigram_count = bigram_count_dict.get(bigram, 0);
        q = 0;
        if bigram_count > 0:
            q = trigram_count / bigram_count;
        if q == 0:
            log_q = -sys.maxsize;
        else:
            log_q = math.log(q, math.e);
        trigram_q_file.write(l.strip() + " " + str(round(log_q, 4)) + "\n");
        l = trigram_file.readline();

    trigram_q_file.close();
    trigram_file.close();


def usage():
    sys.stderr.write("""
    Usage: python 5_1.py ner_rare.counts trigrams.txt > 5_1.txt
        reads in lines of trigrams.txt (yi-2 yi-1 yi)
        produces the file containing trigrams and their respective parameters in the format
        wi−2 wi−1 wi log q(wi|wi−2,wi−1) base on e\n""")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.argv.append("ner_rare.counts")
        sys.argv.append("trigrams.txt");
    elif len(sys.argv) != 3:
        # Expect exactly two argument: the rare count data, the test data file.
        usage();
        sys.exit(2)

    try:
        rare_counts_file = open(sys.argv[1], "r");
        trigram_file = open(sys.argv[2], "r");
        log_q_file = open("5_1.txt","w+");
        compute_trigram_q(rare_counts_file, trigram_file, log_q_file);
    except IOError:
        sys.stderr.write("ERROR: Cannot read input file %s or %s.\n" % sys.argv[1] % sys.argv[2]);
        sys.exit(1)
