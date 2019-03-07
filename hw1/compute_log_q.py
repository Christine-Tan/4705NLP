#! /usr/bin/python3

__author__ = "Xinyue Tan <xt2215"
__date__ = "$Sep 17, 2018"

import math


def compute_log_q(count_file):
    bigram_count_dict, trigram_count_dict = trigram_and_bigram_count(count_file);
    trigram_log_q = dict();
    for trigram in trigram_count_dict.keys():
        bigram = (trigram[0], trigram[1]);
        log_q = math.log(trigram_count_dict[trigram] / bigram_count_dict[bigram], math.e);
        trigram_log_q[trigram] = round(log_q, 4);
    return trigram_log_q;


def trigram_and_bigram_count(count_file):
    trigram_count_dict = dict();
    bigram_count_dict = dict();
    l = count_file.readline();
    while l:
        fields = l.strip().split(" ");
        if fields[1] == "2-GRAM":
            bigram_count_dict[(fields[-2], fields[-1])] = int(fields[0]);
        if fields[1] == "3-GRAM":
            trigram_count_dict[(fields[-3], fields[-2], fields[-1])] = int(fields[0]);
        l = count_file.readline();

    count_file.close();
    return bigram_count_dict, trigram_count_dict;
