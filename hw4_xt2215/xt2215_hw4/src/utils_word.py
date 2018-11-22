from collections import defaultdict


class Word:
    def __init__(self, data_path):
        sentences = open(data_path, 'r').read().strip().split('\n')

        word_id = defaultdict(int)
        id_word = defaultdict(str)
        for sentence in sentences:
            line = sentence.strip().split(' ')
            word_id[line[0]] = int(line[1])
            id_word[int(line[1])] = line[0]

        self.word_id = word_id
        self.id_word = id_word

    def word2id(self, word):
        return self.word_id[word]

    def id2word(self, id):
        return self.id_word[id]

    def num_words(self):
        return len(self.word_id)

