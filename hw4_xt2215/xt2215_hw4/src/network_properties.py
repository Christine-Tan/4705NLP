class NetProperties:
    def __init__(self, word_embed_dim=64, pos_embed_dim=32, label_embed_dim=32, first_hidden_dim=200, second_hidden_dim=200, mini_batch_size=1000):
        self.word_embed_dim = word_embed_dim
        self.pos_embed_dim = pos_embed_dim
        self.label_embed_dim = label_embed_dim
        self.first_hidden_dim = first_hidden_dim
        self.second_hidden_dim = second_hidden_dim
        self.mini_batch_size = mini_batch_size