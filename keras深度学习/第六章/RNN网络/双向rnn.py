"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:反向准确率是一样的
import os
#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""即正反两个rnn，因为数据不一定都是正向更合适，比如倒装句等等"""
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras import layers
from keras.models import Sequential

from keras import optimizers#调整学习率需要先导入

# 视为特征的字数
max_features = 10000
#在此数量的单词之后剪切文本（在最常见的max_features个单词中）
maxlen = 500

# 载入资料
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)

# 反向序列
x_train = [x[::-1] for x in x_train]
x_test = [x[::-1] for x in x_test]
print(x_train)
# 裁剪
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

model = Sequential()
model.add(layers.Embedding(max_features, 32))
model.add(layers.Bidirectional(layers.LSTM(32)))
model.add(layers.Dense(1, activation='sigmoid'))


rmsprop = optimizers.rmsprop(lr=0.5)
model.compile(optimizer=rmsprop,
              loss='binary_crossentropy',
              metrics=['acc'])
history = model.fit(x_train, y_train,
                    epochs=10,
                    batch_size=128,
                    validation_split=0.2)
"""16256/20000是steps_per_epoch的内容，即每次抽取多少内容"""
