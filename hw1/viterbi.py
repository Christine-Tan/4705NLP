#! /usr/bin/python3

__author__ = "Xinyue Tan <xt2215"
__date__ = "$Sep 17, 2018"

import sys
import math
import compute_log_q as lq
import classify_infrequent_word as ciw

"""
using the Viterbi to estimate tagger with the extra log likelihood column
write the result into ner_dev_key
evaluation command: python eval_ne_tagger.py ner_dev.key ner_dev_key
"""


def viterbi(ner_dev_dat, ner_dev_key, standard="RARE"):
    # word (word,tag)->count tag->count
    word_set, word_tag_count_dict, tag_count_dict = get_word_tag_count(standard);
    # tag set, k0={*}, k = set of possible tags
    k0 = {"*"};
    k = tag_count_dict.keys();
    # log q(v|w,u)
    trigram_q_dict = get_trigram_q(standard);

    # tag the dat sentence by sentence
    sentence = [];
    l = ner_dev_dat.readline();
    while l:
        line = l.strip();
        if line:
            sentence.append(line);
        else:
            if len(sentence) > 0:
                tags, probabilities = tag_sentence(sentence, k0, k, word_set, word_tag_count_dict, tag_count_dict,
                                                   trigram_q_dict, standard);
                # write to file
                for i in range(len(sentence)):
                    if probabilities[i] == 0:
                        log_p = sys.float_info.min;
                    else:
                        log_p = probabilities[i]
                    ner_dev_key.write(sentence[i] + " " + tags[i] + " " + str(round(log_p, 4)) + "\n");
                ner_dev_key.write(l);
                # init the sentence
            sentence = [];
        l = ner_dev_dat.readline();

    if len(sentence) > 0:
        tags, probabilities = tag_sentence(sentence, k0, k, word_set, word_tag_count_dict, tag_count_dict,
                                           trigram_q_dict, standard);
        # write the last sentence to file
        for i in range(len(sentence)):
            if probabilities[i] == 0:
                log_p = sys.float_info.min;
            else:
                log_p = probabilities[i];
            ner_dev_key.write(sentence[i] + " " + tags[i] + " " + str(round(log_p, 4)) + "\n");
        ner_dev_key.write(l);
    pass


def tag_sentence(sentence, k0, k, word_set, word_tag_count_dict, tag_count_dict, trigram_q_dict, standard):
    # tag the sentence
    # pi(k,u,v), backpoint bp(k,u,v)
    pi = dict();
    bp = dict();

    n = len(sentence);
    # initial

    init_tuple = (0, "*", "*");
    pi[init_tuple] = 0;
    # loop
    for i in range(1, n + 1):
        kv = k;
        ku = k;
        kw = k;
        if i - 2 <= 0:
            kw = k0;
        if i - 1 <= 0:
            ku = k0;
        # v in kv, u in ku, w in kw
        for v in kv:
            word_tag_tuple = (ciw.classify_by_standard(sentence[i - 1], word_set, standard), v);
            for u in ku:
                index = 0;
                pi_max = -sys.maxsize;
                bp_max = "";
                now_tuple = (i, u, v);

                for w in kw:
                    pre_tuple = (i - 1, w, u);
                    trigram_tuple = (w, u, v);

                    sum_now = pi[pre_tuple];
                    if trigram_tuple in trigram_q_dict.keys():
                        sum_now += trigram_q_dict[trigram_tuple];
                    else:
                        sum_now = -sys.maxsize;

                    if word_tag_tuple in word_tag_count_dict.keys():
                        sum_now += round(math.log(word_tag_count_dict[word_tag_tuple] / tag_count_dict[v], math.e), 4);
                    else:
                        sum_now = -sys.maxsize;

                    if index == 0:
                        pi_max = sum_now;
                        bp_max = w;
                    elif sum_now > pi_max:
                        pi_max = sum_now;
                        bp_max = w;

                    index += 1;
                pi[now_tuple] = pi_max;
                bp[now_tuple] = bp_max;

    # calculate (yn-1,yn)
    pi_max = -sys.maxsize;
    ynp = "";
    yn = "";
    kv = k;
    ku = k;
    index = 0;
    if n - 1 <= 0:
        ku = k0;

    for v in kv:
        for u in ku:
            pre_tuple = (n, u, v);
            trigram_tuple = (u, v, "STOP");
            sum_now = pi[pre_tuple];
            if trigram_tuple in trigram_q_dict.keys():
                sum_now += trigram_q_dict[trigram_tuple];
            if index == 0:
                ynp = u;
                yn = v;
                pi_max = sum_now;
            elif sum_now > pi_max:
                ynp = u;
                yn = v;
                pi_max = sum_now;
            index += 1;

    probability_list = [];
    # tag sequence
    tags = [yn, ynp];
    for k in range(n - 2, 0, -1):
        now_tuple = (k + 2, tags[n - k - 1], tags[n - k - 2]);
        tags.append(bp[now_tuple]);
        probability_list.append(pi[now_tuple]);

    pi2 = (2, tags[n - 1], tags[n - 2]);
    pi1 = (1, "*", tags[n - 1]);
    if n - 2 >= 0:
        probability_list.append(pi[pi2]);
    probability_list.append(pi[pi1]);
    tags = tags[::-1];
    probability_list = probability_list[::-1];
    return tags, probability_list;


def get_trigram_q(standard="RARE"):
    if standard == "RARE":
        counts_file = open("ner_rare.counts", "r");
    else:
        counts_file = open("ner_customize.counts","r");
    trigram_log_q = lq.compute_log_q(counts_file);
    return trigram_log_q;


def get_word_tag_count(standard="RARE"):
    # save word-tag count as dict {(word,tag),count}
    word_tag_count_dict = dict();
    # save tag count as dict{ne, count}
    tag_count_dict = dict();
    # save word set
    word_set = set();

    if standard == "CUSTOMIZE":
        ner_count = open("ner_customize.counts", "r");
    else:
        ner_count = open("ner_rare.counts", "r");

    l = ner_count.readline();
    while l:
        line = l.strip();
        if line:
            fields = line.split(" ");
            if fields[1] == "WORDTAG":
                word = fields[-1];
                tag = fields[2];
                count = int(fields[0]);
                word_tag_count_dict[(word, tag)] = count;
                word_set.add(word);

            elif fields[1] == "1-GRAM":
                tag_count_dict[fields[-1]] = int(fields[0]);
        l = ner_count.readline();

    return word_set, word_tag_count_dict, tag_count_dict;
