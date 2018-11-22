The parameters of network is maintained in parameter.py
The network is defined in network.py
For depModel.py, if the train_data_file is None, it will load the existing model in the model_path, otherwise it
will train the model and save it in the model_path.

Part 1
========================================
Parameters' values:
word_embed_dim = 64
pos_embed_dim = 32
label_embed_dim = 32
first_hidden_dim = 200
second_hidden_dim = 200
mini_batch_size = 1000
epochs = 7

Performance on dev.conll
>> python src/eval.py python src/eval.py trees/dev.conll outputs/dev_part1.conll
Unlabeled attachment score 82.6
Labeled attachment score 79.24

output of test.conll is in outputs/test_part1.conll


Part 2
========================================
Parameters' values:
word_embed_dim = 64
pos_embed_dim = 32
label_embed_dim = 32
first_hidden_dim = 400
second_hidden_dim = 400
mini_batch_size = 1000
epochs = 7

Performance on dev.conll
>> python src/eval.py trees/dev.conll outputs/dev_part2.conll
Unlabeled attachment score 83.44
Labeled attachment score 80.25

output of test.conll is in outputs/test_part2.conll

The model with larger hidden dimensions outperforms that with 200 hidden dimensions because of more hidden units.
The number of hidden units has different optimal values regarding to different number of hidden layers, the input
dimensions, and many other factors.In this case, 400 hidden units is somehow closer to the optimal value.

Part 3
========================================
Parameters' values:
use activation function cube()
word_embed_dim = 256
pos_embed_dim = 32
label_embed_dim = 32
first_hidden_dim = 256
second_hidden_dim = 256
third_hidden_dim = 256
mini_batch_size = 1024
epochs = 7

>> python src/eval.py trees/dev.conll outputs/dev_part3.conll
Unlabeled attachment score 84.58
Labeled attachment score 81.17

output of test.conll is in outputs/test_part3.conll

In this part, I used larger word_embed_dim to better capture the word features.
I also used the cube() function rather than ReLU() as the activation function.
"Intuitively, every hidden unit is computed by a non-linear mapping on a weighted sum of input units plus a bias.
Using g(x) = x^3 can model the product terms of xi*xj*xk for any three different elements at the input layer directly"
Inspired by Chen.D[1], I tried this activation function and the performance was improved by 1% on both UAS and LAS.

References
[1] Chen, D., and Manning, C. A fast and accurate dependency parser using neural networks.
In Proceedings of the 2014 conference on empirical methods in natural language processing
(EMNLP) (2014), pp. 740–750.