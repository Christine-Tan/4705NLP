import json;
import math;
from collections import defaultdict;


class TrainData:
    def __init__(self, train_data, count_file):
        self.terminal_count = dict();
        self.non_terminals_count = dict();
        self.unary_rules_count = dict();
        # binary rules in X -> [(Y1,Z1),(Y2,Z2)...] to speed up the search
        self.binary_rules = defaultdict(list);
        self.binary_rules_count = dict();
        # maximum likelihood for each unary and binary rule
        self.unary_prob = defaultdict(float);
        self.binary_prob = defaultdict(float);

        # count the terminals to decide whether a word is rare word
        self.count_all_terminals(train_data);
        # store all the rules into dict
        self.generate_rules(count_file);
        # calculate the maximum likelihood estimates for each rule parameters
        self.cal_rule_prob();

    def count_terminal(self, tree):
        if len(tree) == 3:
            self.count_terminal(tree[1]);
            self.count_terminal(tree[2]);
        elif len(tree) == 2:
            self.terminal_count.setdefault(tree[1], 0);
            self.terminal_count[tree[1]] += 1;

    # count the terminals to decide whether a word is rare word
    def count_all_terminals(self, train_data):
        for l in open(train_data):
            tree_dict = json.loads(l);
            # count the terminals in this single tree
            self.count_terminal(tree_dict);

    # store all the rules into dict
    def generate_rules(self, count_file):
        for l in open(count_file):
            line = l.strip();
            fields = line.split(' ');
            second = fields[1];
            if second == "NONTERMINAL":
                non_terminal = fields[-1];
                self.non_terminals_count[non_terminal] = int(fields[0]);
            elif second == "UNARYRULE":
                self.unary_rules_count[(fields[-2], fields[-1])] = int(fields[0]);
            elif second == "BINARYRULE":
                binary_rule = (fields[-2], fields[-1]);
                self.binary_rules.setdefault(fields[-3], list());
                self.binary_rules[fields[-3]].append(binary_rule);
                self.binary_rules_count[(fields[-3], fields[-2], fields[-1])] = int(fields[0]);

    # calculate the maximum likelihood estimates for each rule parameters
    def cal_rule_prob(self):
        # calculate the maximum likelihood for each rule
        # all unary rules
        for unary_rule in self.unary_rules_count:
            non_terminal_count = self.non_terminals_count[unary_rule[0]];
            unary_rule_count = self.unary_rules_count[unary_rule];
            # count(X->xi)/count(X)
            prob = round(float(unary_rule_count) / float(non_terminal_count), 6);
            self.unary_prob[unary_rule] = prob;

        # all binary rules
        for binary_rule in self.binary_rules_count:
            non_terminal_count = self.non_terminals_count[binary_rule[0]];
            binary_rule_count = self.binary_rules_count[binary_rule];
            # count(X -> Y Z)/count(X)
            prob = round(float(binary_rule_count) / float(non_terminal_count), 6);
            self.binary_prob[binary_rule] = prob;

    # cky algorithm for one sentence
    def one_cky(self, sentence):
        original_words = sentence.split(' ');

        pi = defaultdict(float);
        bp = defaultdict();

        # substituted words with _RARE_
        words = sentence.split(' ');
        n = len(words);

        for i in range(1, n + 1):
            # substitute word not seen in training data or count<5 with '_RARE_'
            if not words[i - 1] in self.terminal_count:
                words[i - 1] = '_RARE_';

            # init the unary probability for each word
            for x in self.non_terminals_count:
                now_tuple = (i, i, x);
                unary_rule = (x, words[i - 1]);
                pi[now_tuple] = self.unary_prob[unary_rule];

        # cky
        for l in range(1, n):
            for i in range(1, n - l + 1):
                j = i + l;
                # max
                for x in self.non_terminals_count:
                    now_tuple = (i, j, x);

                    max_p = 0.0;
                    binary_rules = self.binary_rules[x];
                    if len(binary_rules) > 0:
                        # loop on the split point
                        for s in range(i, j):
                            # loop on all the possible binary rules start with non-terminal x
                            for binary_rule in binary_rules:
                                y = binary_rule[0];
                                z = binary_rule[1];
                                prob = self.binary_prob[(x, y, z)];
                                pi_left = pi[(i, s, y)];
                                pi_right = pi[(s + 1, j, z)];
                                p = prob * pi_left * pi_right;

                                # save the max and argmax
                                if p > max_p:
                                    max_p = p;
                                    pi[now_tuple] = max_p;
                                    bp[now_tuple] = (y, z, s);

        root = 'S';
        # in case some sentences do not have S as the root
        if pi[(1, n, root)] == 0.0:
            max_p = 0;
            for x in self.non_terminals_count:
                if pi[(1, n, x)] > max_p:
                    max_p = pi[(1, n, x)];
                    root = x;

        # backtrack the parse tree using bp
        parse_tree = self.backtrack(bp, 1, n, root, original_words);
        return parse_tree;

    def backtrack(self, bp, start, end, now_root, words):
        if end == start:
            return [now_root, words[start - 1]];
        else:
            y, z, s = bp[(start, end, now_root)];
            return [now_root, self.backtrack(bp, start, s, y, words), self.backtrack(bp, s + 1, end, z, words)];

    # cky algorithm for the whole file
    def all_cky(self, dev_file, key_file):
        keys = open(key_file, "w+");
        for l in open(dev_file):
            parse_tree = self.one_cky(l.strip());
            keys.write(json.dumps(parse_tree) + '\n');


def cky_algorithm(train_file, count_file, dev_file, key_file):
    data = TrainData(train_file, count_file);
    data.all_cky(dev_file, key_file);
