from collections import defaultdict


class Pos:
    def __init__(self, data_path):
        sentences = open(data_path, 'r').read().strip().split('\n')

        pos_id = defaultdict(int)
        id_pos = defaultdict(str)
        for sentence in sentences:
            line = sentence.strip().split(' ')
            pos_id[line[0]] = int(line[1])
            id_pos[int(line[1])] = line[0]

        self.pos_id = pos_id
        self.id_pos = id_pos

    def pos2id(self, pos):
        return self.pos_id[pos]

    def id2pos(self, id):
        return self.id_pos[id]

    def num_pos(self):
        return len(self.pos_id)