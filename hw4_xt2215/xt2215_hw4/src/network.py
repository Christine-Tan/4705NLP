import dynet as dynet
import random
import matplotlib.pyplot as plt
import numpy as np


class Network:
    def __init__(self, word, pos, label, action, properties):
        self.properties = properties
        self.word = word
        self.pos = pos
        self.label = label
        self.action = action

        # first initialize a computation graph container (or model).
        self.model = dynet.Model()

        # assign the algorithm for backpropagation updates.
        self.updater = dynet.AdamTrainer(self.model)

        # create embeddings for words and tag features.
        self.word_embedding = self.model.add_lookup_parameters((word.num_words(), properties.word_embed_dim))
        self.pos_embedding = self.model.add_lookup_parameters((pos.num_pos(), properties.pos_embed_dim))
        self.label_embedding = self.model.add_lookup_parameters((label.num_labels(), properties.label_embed_dim))

        # assign transfer function
        # self.transfer = dynet.rectify  # can be dynet.logistic or dynet.tanh as well.
        self.transfer = dynet.cube

        # define the input dimension for the embedding layer.
        # here we assume to see 20 word embeddings
        # and to see the 20 pos embeddings and 12 label embeddings
        self.input_dim = 20 * (properties.word_embed_dim + properties.pos_embed_dim) + 12 * properties.label_embed_dim

        # define the first hidden layer.
        self.first_hidden_layer = self.model.add_parameters((properties.first_hidden_dim, self.input_dim))

        # define the second hidden layer.
        self.second_hidden_layer = self.model.add_parameters(
            (properties.second_hidden_dim, properties.first_hidden_dim))

        # define the first hidden layer bias term and initialize it as constant 0.2.
        self.first_hidden_layer_bias = self.model.add_parameters(properties.first_hidden_dim,
                                                                 init=dynet.ConstInitializer(0.2))

        # define the second hidden layer bias term and initialize it as constant 0.2.
        self.second_hidden_layer_bias = self.model.add_parameters(properties.second_hidden_dim,
                                                                  init=dynet.ConstInitializer(0.2))

        # define the output weight.
        self.output_layer = self.model.add_parameters((action.num_actions(), properties.second_hidden_dim))

        # define the bias vector and initialize it as zero.
        self.output_bias = self.model.add_parameters(action.num_actions(), init=dynet.ConstInitializer(0))

    def build_graph(self, word_feat, pos_feat, label_feat):
        # extract word and tags ids
        word_ids = [self.word.word2id(w) for w in word_feat]
        pos_ids = [self.pos.pos2id(p) for p in pos_feat]
        label_ids = [self.label.label2id(l) for l in label_feat]

        # extract word embeddings and tag embeddings from features
        word_embeds = [self.word_embedding[wid] for wid in word_ids]
        pos_embeds = [self.pos_embedding[pid] for pid in pos_ids]
        label_embeds = [self.label_embedding[lid] for lid in label_ids]

        # concatenating all features (recall that '+' for lists is equivalent to appending two lists)
        embedding_layer = dynet.concatenate(word_embeds + pos_embeds + label_embeds)

        # calculating the first hidden layer
        first_hidden = self.transfer(self.first_hidden_layer * embedding_layer + self.first_hidden_layer_bias)
        # calculating the second hidden layer
        second_hidden = self.transfer(self.second_hidden_layer * first_hidden + self.second_hidden_layer_bias)

        # calculating the output layer
        output = self.output_layer * second_hidden + self.output_bias

        # return the output as a dynet vector
        return output

    def train(self, train_file, epochs):
        # matplotlib config
        loss_values = []
        plt.ion()
        ax = plt.gca()
        ax.set_xlim([0, 10])
        ax.set_ylim([0, 3])
        plt.title("Loss over time")
        plt.xlabel("Minibatch")
        plt.ylabel("Loss")

        for i in range(epochs):
            print('started epoch', (i + 1))
            losses = []
            train_data = open(train_file, 'r').read().strip().split('\n')

            # shuffle the training data.
            random.shuffle(train_data)

            step = 0
            for line in train_data:
                fields = line.strip().split(' ')
                word_feat, pos_feat, label_feat, action = fields[0:20], fields[20:40], fields[40:52], fields[-1]
                gold_label = self.action.action2id(action)

                result = self.build_graph(word_feat, pos_feat, label_feat)
                # result = self.dropout(result, self.dropout_rate)

                # getting loss with respect to negative log softmax function and the gold label.
                loss = dynet.pickneglogsoftmax(result, gold_label)

                # appending to the minibatch losses
                losses.append(loss)
                step += 1

                if len(losses) >= self.properties.mini_batch_size:
                    # now we have enough loss values to get loss for minibatch
                    minibatch_loss = dynet.esum(losses) / len(losses)

                    # calling dynet to run forward computation for all minibatch items
                    minibatch_loss.forward()

                    # getting float value of the loss for current minibatch
                    minibatch_loss_value = minibatch_loss.value()

                    # printing info and plotting
                    loss_values.append(minibatch_loss_value)
                    if len(loss_values) % 10 == 0:
                        ax.set_xlim([0, len(loss_values) + 10])
                        ax.plot(loss_values)
                        plt.draw()
                        plt.pause(0.0001)
                        progress = round(100 * float(step) / len(train_data), 2)
                        print('current minibatch loss', minibatch_loss_value, 'progress:', progress, '%')

                    # calling dynet to run backpropagation
                    minibatch_loss.backward()

                    # calling dynet to change parameter values with respect to current backpropagation
                    self.updater.update()

                    # empty the loss vector
                    losses = []

                    # refresh the memory of dynet
                    dynet.renew_cg()

            # there are still some minibatch items in the memory but they are smaller than the minibatch size
            # so we ask dynet to forget them
            dynet.renew_cg()

    def load(self, filename):
        self.model.populate(filename)

    def save(self, filename):
        self.model.save(filename)
