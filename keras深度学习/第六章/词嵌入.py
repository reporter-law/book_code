"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:预训练词向量反应高维词数据的变动，只是换了低维表示而已
"""预训练词向量效果不明显，本书是说由于样本量只有200"""
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
training_samples = 200  # W我们将训练200个样本
""" 因为预先培训过的单词嵌入在培训数据很少的问题上特别有用（否则，特定于任务的嵌入可能会优于它们），
我们将添加以下限制：我们将培训数据限制在前200个样本。因此，我们将学习分类电影评论后，只看了200个例子…"""
validation_samples = 10000  # 我们将验证10000个样本
max_words = 10000  # 我们只会考虑数据集中的前10,000个单词，
"""# 单词不会重复"""

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)#转为索引列表
print(len(sequences[0]),len(texts))#样本数量
"""[62, 4, 3, 129, 34, 44, 7576, 1414, 15, 3, 4252, 514, 43, 16, 3, 633, 133, 12, 6, 3, 1301, 459, 4, 1751, 209, 3, 7693,
 308, 6, 676, 80, 32, 2137, 1110, 3008, 31, 1, 929, 4, 42, 5120, 469, 9, 2665, 1751, 1, 223, 55, 16, 54, 828, 1318, 847, 
 228, 9, 40, 96, 122, 1484, 57, 145, 36, 1, 996, 141, 27, 676, 122, 1, 411, 59, 94, 2278, 303, 772, 5, 3, 837, 20, 3, 
 1755, 646, 42, 125, 71, 22, 235, 101, 16, 46, 49, 624, 31, 702, 84, 702, 378, 3493, 2, 8422, 67, 27, 107, 3348]"""
word_index = tokenizer.word_index
#print(word_index)
"""{'muppified': 88581, 'hued': 88582}样式的字典"""
print('Found %s unique tokens.' % len(word_index))

data = pad_sequences(sequences, maxlen=maxlen)#索引张量化,目的是进行长短裁剪填充保障长度相同
"""(len(sequences), maxlen),样本数量和裁剪后的长度"""
print(len(data[0]))
"""[  34   44 7576 1414   15    3 4252  514   43   16    3  633  133   12
     6    3 1301  459    4 1751  209    3 7693  308    6  676   80   32
  2137 1110 3008   31    1  929    4   42 5120  469    9 2665 1751    1
   223   55   16   54  828 1318  847  228    9   40   96  122 1484   57
   145   36    1  996  141   27  676  122    1  411   59   94 2278  303
   772    5    3  837   20    3 1755  646   42  125   71   22  235  101
    16   46   49  624   31  702   84  702  378 3493    2 8422   67   27
   107 3348]"""
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

embedding_matrix = np.zeros((max_words, embedding_dim))
for word, i in word_index.items():
    #从分词词典中寻找预训练词向量词典中向量
    embedding_vector = embeddings_index.get(word)
    if i < max_words:
        if embedding_vector is not None:
            # 在嵌入索引中找不到的单词将为全零,因为本身就是一个全0的张量
            embedding_matrix[i] = embedding_vector
print(embedding_matrix)


#定义一个网络
from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense

model = Sequential()
"""词嵌入使得单词具有向量但是不等于单词，只是对词进行降维"""
model.add(Embedding(max_words, embedding_dim, input_length=maxlen))#多少个词，多少维度
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.summary()
"""这是展示网络层输出数据张量，(None, 100, 100) 表示embedding样本为0，但是是一个100个单词100个维度的张量，一词100维度"""
#加载预训练词向量
model.layers[0].set_weights([embedding_matrix])
"""第1层就是embedding层"""
model.layers[0].trainable = False

#编译执行
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['acc'])
history = model.fit(x_train, y_train,
                    epochs=10,
                    batch_size=32,
                    validation_data=(x_val, y_val))
model.save_weights('J:\PyCharm项目\学习进行中\keras深度学习\model\pre_trained_glove_model.h5')

#绘图
import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()