#! /usr/bin/python

__author__ = "Alexander Rush <srush@csail.mit.edu>"
__date__ = "$Sep 12, 2012"

import json
import sys
import os
import cky

"""
replace infrequent words Count(x)<5 in parse_train.dat
into parse_train.RARE.dat
"""


class Tree:
    def __init__(self):
        self.terminal_count = {};

    def count_terminal(self, tree):
        if len(tree) == 3:
            self.count_terminal(tree[1]);
            self.count_terminal(tree[2]);
        elif len(tree) == 2:
            self.terminal_count.setdefault(tree[1], 0);
            self.terminal_count[tree[1]] += 1;

    def replace_with_rare(self, tree, rare_terminals):
        if len(tree) == 3:
            self.replace_with_rare(tree[1], rare_terminals);
            self.replace_with_rare(tree[2], rare_terminals);
        elif len(tree) == 2:
            if tree[1] in rare_terminals:
                tree[1] = "_RARE_";


def count_all_terminals(original_dat):
    all_terminal_count = dict();
    for l in open(original_dat):
        tree_dict = json.loads(l);
        tree = Tree();
        # count the terminals in this single tree
        tree.count_terminal(tree_dict);
        terminal_count = tree.terminal_count;
        # add them into the all_terminal_count
        for terminal in terminal_count:
            all_terminal_count.setdefault(terminal, 0);
            all_terminal_count[terminal] += 1;
    return all_terminal_count;


def get_rare_terminals(original_dat):
    all_terminal_count = count_all_terminals(original_dat);
    rare_terminals = set();
    for terminal in all_terminal_count:
        if all_terminal_count[terminal] < 5:
            rare_terminals.add(terminal);
    return rare_terminals;


def replace_infrequent(original_dat, rare_dat):
    rare_terminals = get_rare_terminals(original_dat);
    rare_dat = open(rare_dat, "w+");

    for l in open(original_dat):
        tree_dict = json.loads(l);
        tree = Tree();
        tree.replace_with_rare(tree_dict, rare_terminals);
        rare_dat.write(json.dumps(tree_dict) + '\n');


def usage():
    sys.stderr.write("""
    Usage: python parser.py q4 parse_train.dat parse_train.RARE.dat
        Substitute all the words in count_file which has count(word)<5
        into parse_train.RARE.dat.\n""")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        usage();
        sys.exit(2)

    try:
        question = sys.argv[1];
        if question == 'q4':
            # replace infrequent word with count(x)<5
            ori_dat_file = sys.argv[2];
            rare_dat_file = sys.argv[3];
            replace_infrequent(ori_dat_file, rare_dat_file);
            count_file = rare_dat_file + '.count';
            os.system("python count_cfg_freq.py %s > %s\n" % (rare_dat_file, count_file));
        if question == 'q5':
            rare_dat_file = sys.argv[2];
            count_file = rare_dat_file + '.count';
            dev_dat_file = sys.argv[3];
            key_file = sys.argv[4];
            cky.cky_algorithm(rare_dat_file, count_file, dev_dat_file, key_file);
        if question == 'q6':
            rare_dat_file = sys.argv[2];
            count_file = rare_dat_file + '.count';
            dev_dat_file = sys.argv[3];
            key_file = sys.argv[4];
            cky.cky_algorithm(rare_dat_file, count_file, dev_dat_file, key_file);
    except IOError:
        sys.stderr.write("ERROR: Cannot read input file %s or %s.\n" % (sys.argv[2], sys.argv[3]));
        sys.exit(1)
