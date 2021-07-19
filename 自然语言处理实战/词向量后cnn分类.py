# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os, warnings

warnings.filterwarnings("ignore")
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import glob
import os

from random import shuffle


def pre_process_data(filepath):
    """
    This is dependent on your training data source but we will try to generalize it as best as possible.
    """
    positive_path = os.path.join(filepath, 'pos')
    negative_path = os.path.join(filepath, 'neg')

    pos_label = 1
    neg_label = 0

    dataset = []

    for filename in glob.glob(os.path.join(positive_path, '*.txt')):
        with open(filename, 'r',encoding="utf-8") as f:
            dataset.append((pos_label, f.read()))

    for filename in glob.glob(os.path.join(negative_path, '*.txt')):
        with open(filename, 'r',encoding="utf-8") as f:
            dataset.append((neg_label, f.read()))
    """形成标签 内容列表类似于[（1 大大大大大大大大大）
    (2 dadadadadada)]"""
    shuffle(dataset)

    return dataset


dataset = pre_process_data(r'J:\PyCharm项目\学习进行中\自然语言处理实战\nlpia_master_\nlpia_master\src\nlpia\aclImdb\train')
print(dataset[0])


# In[ ]:
"""
from gensim.models import word2vec

# 加载模型
model_name = 'Domain-Word2vec.model' 
# 嵌入向量维度
Embedding_dim = 100
embedding_model = word2vec.Word2Vec.load(model_name)

word2idx = {'PAD': 0}
# 所有词对应的嵌入向量 [(word, vector)]
vocab_list = [(k, embedding_model.wv[k]) for k, v in embedding_model.wv.vocab.items()]
# [len(vocab)+1, embedding_dim] '+1'是增加了一个'PAD'
embeddings_matrix = np.zeros((len(embedding_model.wv.vocab.items()) + 1,\
 								embedding_model.vector_size))
# word2idx 字典
for i in range(len(vocab_list)):
    word = vocab_list[i][0]
    word2idx[word] = i + 1
    embeddings_matrix[i + 1] = vocab_list[i][1]

# 初始化keras中的Embedding层权重
embedding = Embedding(input_dim=len(embeddings_matrix),
                  output_dim=Embedding_dim,
                  weights=[embeddings_matrix], # 预训练参数
                  trainable=False)
"""

from nltk.tokenize import TreebankWordTokenizer
from gensim.models import KeyedVectors
word_vectors = KeyedVectors.load_word2vec_format(r'J:\PyCharm项目\学习进行中\自然语言处理实战\nlpia_master_\nlpia_master\src\nlpia\model\GoogleNews-vectors-negative300.bin.gz', binary=True, limit=200000)


def tokenize_and_vectorize(dataset):
    tokenizer = TreebankWordTokenizer()
    vectorized_data = []
    expected = []
    for sample in dataset:
        tokens = tokenizer.tokenize(sample[1])
        """分词"""
        sample_vecs = []
        for token in tokens:
            try:
                """分词后获得词向量"""
                sample_vecs.append(word_vectors[token])

            except KeyError:
                pass  # No matching token in the Google w2v vocab

        vectorized_data.append(sample_vecs)

    return vectorized_data


# In[ ]:


def collect_expected(dataset):
    """ Peel of the target values from the dataset """
    expected = []
    for sample in dataset:
        expected.append(sample[0])
    return expected


# In[ ]:


vectorized_data = tokenize_and_vectorize(dataset)
expected = collect_expected(dataset)


# In[ ]:


split_point = int(len(vectorized_data) * .8)#0.8

x_train = vectorized_data[:split_point]
y_train = expected[:split_point]
x_test = vectorized_data[split_point:]
y_test = expected[split_point:]


# In[ ]:


maxlen = 400
batch_size = 32         # How many samples to show the net before backpropogating the error and updating the weights
embedding_dims = 300    # Length of the token vectors we will create for passing into the Convnet
filters = 250           # Number of filters we will train
kernel_size = 3         # The width of the filters, actual filters will each be a matrix of weights of size: embedding_dims x kernel_size or 50 x 3 in our case
hidden_dims = 250       # Number of neurons in the plain feed forward net at the end of the chain
epochs = 2              # Number of times we will pass the entire training dataset through the network


# In[ ]:


# Must manually pad/truncate

def pad_trunc(data, maxlen):
    """ For a given dataset pad with zero vectors or truncate to maxlen """
    new_data = []

    # Create a vector of 0's the length of our word vectors
    zero_vector = []
    for _ in range(len(data[0][0])):
        zero_vector.append(0.0)

    for sample in data:

        if len(sample) > maxlen:
            temp = sample[:maxlen]
        elif len(sample) < maxlen:
            temp = sample
            additional_elems = maxlen - len(sample)
            for _ in range(additional_elems):
                temp.append(zero_vector)
        else:
            temp = sample
        new_data.append(temp)
    return new_data


# In[ ]:


x_train = pad_trunc(x_train, maxlen)
x_test = pad_trunc(x_test, maxlen)

x_train = np.reshape(x_train, (len(x_train), maxlen, embedding_dims))
y_train = np.array(y_train)
x_test = np.reshape(x_test, (len(x_test), maxlen, embedding_dims))
y_test = np.array(y_test)


# In[ ]:


print('Build model...')
model = Sequential()

# we add a Convolution1D, which will learn filters
# word group filters of size filter_length:
model.add(Conv1D(filters,
                 kernel_size,
                 padding='valid',
                 activation='relu',
                 strides=1,
                 input_shape=(maxlen, embedding_dims)))
# we use max pooling:
model.add(GlobalMaxPooling1D())
# We add a vanilla hidden layer:
model.add(Dense(hidden_dims))
model.add(Dropout(0.2))
model.add(Activation('relu'))
# We project onto a single unit output layer, and squash it with a sigmoid:
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test))
model_structure = model.to_json()
with open("cnn_model.json", "w") as json_file:
    json_file.write(model_structure)

model.save_weights("cnn_weights.h5")
print('Model saved.')
