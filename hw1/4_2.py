#! /usr/bin/python3

__author__ = "Xinyue Tan <xt2215>"
__date__ = "$Sep 17, 2018"

import math
import sys
import os

"""
use ner_rare.counts file to compute arg max e(x|y)
produces the tagged ner_dev.dat with the extra log likelihood column
write the result into 4_2.txt
evaluation command: python eval_ne_tagger.py ner_dev.key 4_2.txt
"""


def compute_emission(ner_rare_count, ner_dev_dat, ner_dev_key):
    # save word-ne count as dict {word,list(ne,count)}
    count_word_ne_dict = dict();
    # save ne count as dict{ne, count}
    count_ne_dict = dict();
    l = ner_rare_count.readline();
    while l:
        line = l.strip();
        if line:
            fields = line.split(" ");
            if fields[1] == "WORDTAG":
                word = fields[-1];
                ne_count = (fields[2], int(fields[0]));
                temp_list = count_word_ne_dict.setdefault(word, list());
                temp_list.append(ne_count);
                count_word_ne_dict[word] = temp_list;

            elif fields[1] == "1-GRAM":
                count_ne_dict[fields[-1]] = int(fields[0]);
        l = ner_rare_count.readline();

    ner_rare_count.close();
    # compute emission & write to 4_2.txt
    l = ner_dev_dat.readline();
    while l:
        word = l.strip();
        if word:
            ne_count_list = count_word_ne_dict.get(word, count_word_ne_dict.get("_RARE_"));

            max_ne = "O";
            max_e = 0;
            for ne_count in ne_count_list:
                ne = ne_count[0];
                word_ne_count = ne_count[1];
                ne_count = count_ne_dict.get(ne, 0);
                emission = 0;
                if ne_count > 0:
                    emission = word_ne_count / ne_count;
                if emission > max_e:
                    max_e = emission;
                    max_ne = ne;
            # log probability
            if max_e == 0:
                log_e = -sys.maxsize;
            else:
                log_e = math.log(max_e, math.e);
            ner_dev_key.write(word + " " + max_ne + " " + str(round(log_e, 4)) + "\n");
        else:
            ner_dev_key.write(l);
        l = ner_dev_dat.readline();

    ner_dev_dat.close();
    ner_dev_key.close();
    pass


def usage():
    sys.stderr.write("""
    Usage: python 4_2.py ner_rare.counts ner_dev.dat > 4_2.txt
        use ner_rare.counts file to compute arg max e(x|y)
        produces the tagged ner_dev.dat with the extra log likelihood column
        write the result into 4_2.txt\n""")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.argv.append("ner_rare.counts")
        sys.argv.append("ner_dev.dat");
    elif len(sys.argv) != 3:
        # Expect exactly two argument: the rare count data, the test data file.
        usage();
        sys.exit(2)

    try:
        rare_counts_file = open(sys.argv[1], "r");
        test_data_file = open(sys.argv[2], "r");
        ner_key_file = open("4_2.txt", "w+");
        compute_emission(rare_counts_file, test_data_file, ner_key_file);
    except IOError:
        sys.stderr.write("ERROR: Cannot read input file %s or %s.\n" % sys.argv[1] % sys.argv[2]);
        sys.exit(1)
