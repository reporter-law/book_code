"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
from keras.datasets import reuters

(train_data, train_labels), (test_data, test_labels) = reuters.load_data(num_words=10000)#导入的数据量
word_index = reuters.get_word_index()#调用index下载实际数据#557056/550378 [==============================] - 1s 1us/step
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
# 请注意，我们的索引偏移了3，因为0、1和2是“填充”，“序列开始”和“未知”的保留索引。
decoded_newswire = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])
print(decoded_newswire)
"""该公司表示，由于其12月收购space co的结果，预计1987年的每股收益为1 -15至1 30 dlrs，高于1986年的70 cts。
该公司表示，税前净利润应从600万dlr增至9到1000万dlr 1986年，租赁业务收入从1200万到5200万迪拉姆，增至19到2200万迪拉姆，
它说，今年的每股现金流应为2 50到3 dlrs路透社3
"""
#数据编码
import numpy as np

#x数据向量化，变成，有小数点的，这是one-hot编码，每一行一万个词表，存在设为i1，不存在为0
def vectorize_sequences(sequences, dimension=10000):#尺寸
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results
x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)
#标签向量化
def to_one_hot(labels, dimension=46):
    results = np.zeros((len(labels), dimension))
    for i, label in enumerate(labels):
        results[i, label] = 1.
    return results
one_hot_train_labels = to_one_hot(train_labels)
one_hot_test_labels = to_one_hot(test_labels)

"""这是在重复标签向量化的过程，只是这个方法是内置的：文字标签整数化，整数标签向量化"""
from keras.utils.np_utils import to_categorical
one_hot_train_labels = to_categorical(train_labels)#
one_hot_test_labels = to_categorical(test_labels)



"""正式的深度学习网络构建"""
from keras import models
from keras import layers
"""
model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(64, activation='relu'))
'''与之一不同的地方在于，最终输出'''
model.add(layers.Dense(46, activation='softmax'))
model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
#准备数据
x_val = x_train[:1000]
partial_x_train = x_train[1000:]

y_val = one_hot_train_labels[:1000]
partial_y_train = one_hot_train_labels[1000:]

#开始训练
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=3,
                    batch_size=512,
                    validation_data=(x_val, y_val))


import matplotlib.pyplot as plt

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(loss) + 1)

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()


#准确率图plt.clf()   # clear figure

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()
"""

#验证后重新训练
model = models.Sequential()
model.add(layers.Dense(128, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(128, activation='relu'))#隐藏神经元尽量要比输出大，否者导致准确度下降！！！！！！！！！！
model.add(layers.Dense(46, activation='softmax'))

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
#准备数据
x_val = x_train[:1000]
partial_x_train = x_train[1000:]

y_val = one_hot_train_labels[:1000]
partial_y_train = one_hot_train_labels[1000:]

#开始un
model.fit(partial_x_train,
          partial_y_train,
          epochs=8,
          batch_size=512,
          validation_data=(x_val, y_val))
results = model.evaluate(x_test, one_hot_test_labels)#结果

#进行预测
predictions = model.predict(x_test)
predict_test = model.predict_classes(x_test).astype('int')
print(predict_test[0])
print(np.argmax(predictions[0]))#返回预测的最大概率的类别
np.sum(predictions[0])
np.argmax(predictions[0])
"""若不向量化，则修改损失函数"""
loss='sparse_categorical_crossentropy'