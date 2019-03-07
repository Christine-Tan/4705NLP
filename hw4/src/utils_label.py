from collections import defaultdict


class Label:
    def __init__(self, data_path):
        sentences = open(data_path, 'r').read().strip().split('\n')

        label_id = defaultdict(int)
        id_label = defaultdict(str)
        for sentence in sentences:
            line = sentence.strip().split(' ')
            label_id[line[0]] = int(line[1])
            id_label[int(line[1])] = line[0]

        self.label_id = label_id
        self.id_label = id_label

    def label2id(self, label):
        return self.label_id[label]

    def id2label(self, id):
        return self.id_label[id]

    def num_labels(self):
        return len(self.label_id)