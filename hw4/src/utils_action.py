from collections import defaultdict


class Action:
    def __init__(self, data_path):
        sentences = open(data_path, 'r').read().strip().split('\n')

        action_id = defaultdict(int)
        id_action = defaultdict(str)
        for sentence in sentences:
            line = sentence.strip().split(' ')
            action_id[line[0]] = int(line[1])
            id_action[int(line[1])] = line[0]

        self.action_id = action_id
        self.id_action = id_action

    def action2id(self, action):
        return self.action_id[action]

    def id2action(self, id):
        return self.id_action[id]

    def num_actions(self):
        return len(self.action_id)