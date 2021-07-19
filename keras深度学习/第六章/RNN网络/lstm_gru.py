"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:理解：当前输入不是数值而是权重
import os
#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""lstm:遗忘门：遗忘门能决定应丢弃或保留哪些信息。来自先前隐藏状态的信息和当前输入的信息同时输入到Sigmoid函数，输出值处于0和1之间，越接近0意味着越应该忘记，越接近1意味着越应该保留。（即sigmoid数值缩放，丢掉0）
lstm:输入门：输入门用来更新单元状态。第一步：先将先前隐藏状态的信息和当前输入的信息输入到Sigmoid函数，在0和1之间调整输出值来决定更新哪些信息，0表示不重要，1表示重要。
第二步：也可将隐藏状态和当前输入传输给Tanh函数，并在-1和1之间压缩数值以调节网络，
第三步：然后把Tanh输出和Sigmoid输出相乘，Sigmoid输出将决定在Tanh输出中哪些信息是重要的且需要进行保留。
传给c
lstm:输出门：输出门能决定下个隐藏状态的值，隐藏状态中包含了先前输入的相关信息。
首先把先前的隐藏状态和当前输入传递给Sigmoid函数；接着把新得到的单元状态传递给Tanh函数；
然后把Tanh输出和Sigmoid输出相乘，以确定隐藏状态应携带的信息；
最后把隐藏状态作为当前单元输出，把新的单元状态和新的隐藏状态传输给下个时间步
重要的是sigmoid进行选择丢掉为0 的数值，ht是当前预测的输出

实质：就是多了一个sigmoid
理解：当前输入不是数值而是权重！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
遗忘：即当前输入与之前输入的求sigmoid，计算上一个权重中哪些要丢弃
输入门：当前与之前权重合集求sigmoi遗忘规律并和当前压缩到tanh范围的权重进行计算当前需要丢弃的内容
输出门：继续利用当前与之前权重合集求sigmoi遗忘规律，用这一规律求已经更新过的前一个权重与当前权重的和，作为下一个输入值（这是在保存之前信息）
好处：精度高，使用数据量少
"""
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Embedding

max_features = 10000  # 视为特征的字数
maxlen = 1000  # 在此数目的单词之后剪切文本（在最常见的max_features个单词中）
batch_size = 32

print('Loading data...')
(input_train, y_train), (input_test, y_test) = imdb.load_data(num_words=max_features)
print(len(input_train), 'train sequences')
"""[1, 194, 1153, 194, 8255,已经索引化了"""
print(len(input_test), 'test sequences',input_test)

print('Pad sequences (samples x time)')
input_train = sequence.pad_sequences(input_train, maxlen=maxlen)#裁剪
input_test = sequence.pad_sequences(input_test, maxlen=maxlen)
print('input_train shape:', input_train.shape)
print('input_test shape:', input_test.shape)

#lstm
from keras.layers import LSTM
from keras.layers import Dense

model = Sequential()
model.add(Embedding(max_features, 32))
model.add(LSTM(32))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['acc'])
history = model.fit(input_train, y_train,
                    epochs=10,
                    batch_size=128,
                    validation_split=0.2)
#绘图
import matplotlib.pyplot as plt
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

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
