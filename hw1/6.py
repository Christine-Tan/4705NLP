#! /usr/bin/python3

__author__ = "Xinyue Tan <xt2215"
__date__ = "$Sep 17, 2018"

import classify_infrequent_word as ciw
import sys
import viterbi as v
import os

"""
the tagged ner_dev.dat data in the same format as 4_2.txt and 5_2.txt 
using the your improved Viterbi tagger that better deals with rare words.
"""


def tag_rare(ori_counts_dat, ori_train, rare_train):
    # read in lines of ner.counts of original training data
    rare_list = [];
    nl = ori_counts_dat.readline();
    while nl:
        line = nl.strip();
        if line:
            fields = line.split(" ");
            tag = fields[1];
            count = int(fields[0]);
            if tag == "WORDTAG" and count < 5:
                # (word, tag)
                rare_list.append((fields[-1], fields[-2]));
        nl = ori_counts_dat.readline();

    ori_counts_dat.close();
    # read in lines of ner_train.dat
    # rewrite the classified word in rare_set into ner_train_customize.dat
    nl = ori_train.readline();
    while nl:
        line = nl.strip();
        if line:
            fields = line.split(" ");
            word = fields[0];
            tag = fields[-1];
            if (word, tag) in rare_list:
                substitute = ciw.classify_infrequent_word_customized(word, set());
                rare_train.write(substitute + " " + tag + "\n");
            else:
                rare_train.write(nl);
        else:
            rare_train.write(nl);
        nl = ori_train.readline();

    ori_train.close();
    rare_train.close();

    pass


def usage():
    sys.stderr.write("""
    Usage: python 6.py [test_file] > [6.txt]
        using the Viterbi to estimate tagger with the extra log likelihood column
        write the result into 6.txt
        dealing with infrequent words with customized rules\n""")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.argv.append("ner_dev.dat")
    elif len(sys.argv) != 2:
        # Expect exactly three argument: the original count data, the training data file, the new rare train file
        usage();
        sys.exit(2)

    try:
        ori_counts_file = open("ner.counts", "r");
        ori_train_file = open("ner_train.dat", "r");
        rare_train = open("ner_train_customize.dat", "w+");
        tag_rare(ori_counts_file, ori_train_file, rare_train);
        os.system("python count_freqs.py ner_train_customize.dat > ner_customize.counts")

        ner_dev_dat = open(sys.argv[1], "r");
        ner_dev_key = open("6.txt","w+");
        v.viterbi(ner_dev_dat, ner_dev_key, "CUSTOMIZE");

    except IOError:
        sys.stderr.write("ERROR: Cannot read input file %s or %s.\n" % sys.argv[1] % sys.argv[2]);
        sys.exit(1)
