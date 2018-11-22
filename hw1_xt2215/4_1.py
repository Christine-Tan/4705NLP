#! /usr/bin/python3

__author__ = "Xinyue Tan <xt2215"
__date__ = "$Sep 17, 2018"

import sys;
import os;

"""
Replace infrequent words(Count(x)<5) in ner_train.dat with symbol _RARE_
rewrite the training data with symbol _RARE_ into a new file ner_train_rare.dat
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
    # rewrite the tag of word in rare_set into _RARE_ into ner_train_rare.dat
    nl = ori_train.readline();
    while nl:
        line = nl.strip();
        if line:
            fields = line.split(" ");
            word = fields[0];
            tag = fields[-1];
            if (word, tag) in rare_list:
                rare_train.write("_RARE_ " + tag + "\n")
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
    Usage: python 4_1.py ner.counts ner_train.dat > ner_train_rare.dat
        Substitute all the words in count_file which has count(word)<5
        into _RARE_. Rewrite the train_file with substituted words.\n""")


if __name__ == "__main__":
    if len(sys.argv) <=1:
        sys.argv.append("ner.counts")
        sys.argv.append("ner_train.dat");
    elif len(sys.argv) != 3:
        # Expect exactly two argument: the rare count data, the test data file.
        usage();
        sys.exit(2)

    try:
        ori_counts_file = open(sys.argv[1], "r");
        ori_train_file = open(sys.argv[2], "r");
        rare_train_file = open("ner_train_rare.dat","w+");
        tag_rare(ori_counts_file, ori_train_file, rare_train_file);

    except IOError:
        sys.stderr.write("ERROR: Cannot read input file %s or %s.\n" % sys.argv[1] % sys.argv[2]);
        sys.exit(1)
