"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"



imdb_dir = r'J:\PyCharm项目\学习书籍成果\keras深度学习\data\aclImdb'
train_dir = os.path.join(imdb_dir, 'train')
labels = []
texts = []
for label_type in ['neg', 'pos']:
    dir_name = os.path.join(train_dir, label_type)
    for fname in os.listdir(dir_name):
        if fname[-4:] == '.txt':
            f = open(os.path.join(dir_name, fname),encoding="utf-8")
            texts.append(f.read())
            f.close()
            if label_type == 'neg':
                labels.append(0)
            else:
                labels.append(1)



from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

maxlen = 100  #我们将在100个单词后删除评论
training_samples = 200
validation_samples = 10000  # 我们将验证10000个样本
max_words = 10000  # 我们只会考虑数据集中的前10,000个单词，
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)#转为索引列表
print(len(sequences[0]),len(texts))#样本数量
word_index = tokenizer.word_index
#print(word_index)
"""{'muppified': 88581, 'hued': 88582}样式的字典"""
print('Found %s unique tokens.' % len(word_index))

data = pad_sequences(sequences, maxlen=maxlen)#索引张量化,目的是进行长短裁剪填充保障长度相同
"""(len(sequences), maxlen),样本数量和裁剪后的长度"""
print(len(data[0]))
labels = np.asarray(labels)
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)


'''小结上述过程，分词，映射为索引，对索引进行裁剪形成样本数量与文本裁剪的张量'''
# 将数据分为训练集和验证集。但是，首先，将数据混洗，因为我们从有序采样的数据开始（首先全部为负，然后全部为正）。
indices = np.arange(data.shape[0])#对250000条评论进行打乱？？？？？？
print(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]

"""只提取前200个分好词的样本"""
x_train = data[:training_samples]
y_train = labels[:training_samples]
x_val = data[training_samples: training_samples + validation_samples]
y_val = labels[training_samples: training_samples + validation_samples]

#加载预训练模型,构建向量表
glove_dir = 'J:\PyCharm项目\学习书籍成果\keras深度学习\data\glove'
embeddings_index = {}
f = open(os.path.join(glove_dir, 'glove.6B.100d.txt'),encoding="utf-8")
for line in f:
    values = line.split()

    word = values[0]#这是一个单词
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs#形成字典
f.close()

print('Found %s word vectors.' % len(embeddings_index))

#嵌入矩阵
embedding_dim = 100#词向量的维度
max_words = 10000
embedding_matrix = np.zeros((max_words, embedding_dim))
for word, i in word_index.items():
    #从分词词典中寻找预训练词向量词典中向量
    embedding_vector = embeddings_index.get(word)
    if i < max_words:
        if embedding_vector is not None:
            # 在嵌入索引中找不到的单词将为全零,因为本身就是一个全0的张量
            embedding_matrix[i] = embedding_vector
#print(embedding_matrix)


#定义一个网络
from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense



#模型
from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop
model = Sequential()
"""词嵌入使得单词具有向量但是不等于单词，只是对词进行降维"""
model.add(Embedding(max_words, embedding_dim, input_length=maxlen))#多少个词，多少维度
model.add(layers.Conv1D(32, 5, activation='relu'))
model.add(layers.MaxPooling1D(3))
model.add(layers.Conv1D(32, 5, activation='relu'))#池化就是一中丢弃式的展平
"""可以直接搭rnn???????????,池化后就是二维张量"""
model.add(layers.GRU(32, dropout=0.1, recurrent_dropout=0.5))
model.add(layers.Dense(1))
#加载预训练词向量
model.layers[0].set_weights([embedding_matrix])
"""第1层就是embedding层"""
model.layers[0].trainable = False
model.summary()
#编译执行
model.compile(optimizer='rmsprop',loss='binary_crossentropy', metrics=['acc'])
history = model.fit(x_train, y_train,epochs=10,batch_size=32,validation_data=(x_val, y_val))
