"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:尝试增加层数、隐藏节点数、更换损失函数、激活函数、训练轮次
"""
层：将输入张量变换为一个以上的张量；2d张量用dense这个密集层（全连接层);3d张量用循环层lstm层；4d张量用二维卷积层（conv2d层）
损失函数：即为评价方法，与数据有关，并不是最小最好，函数不一样？？？
"""
from keras import models#算法模型
from keras import layers#神经网络层
import warnings
warnings.filterwarnings("ignore")

model = models.Sequential()#网络结构决定了假设空间，这是线性堆叠方式
model.add(layers.Dense(32,input_shape=(784,)))#32是维度即输出多少个结果即神经网络的层数即次数，input_shape是输入数据的大小，一次多少样本数量不在这里！！而是batch_size
model.add(layers.Dense(32))




from keras.datasets import imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
#print(train_data[0])
#print(train_data[1])


word_index = imdb.get_word_index()

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])
#print(decoded_review)
#已被编码过了，所以只有index,而没有实际内容，需要进行转化


"""整数编码二进制化"""
import numpy as np

def vectorize_sequences(sequences, dimension=10000):
    # 创建一个全零形状的矩阵（len（序列），尺寸）
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.  #将结果的特定索引[i]设置为1s
    return results

# 我们的矢量化训练数据
x_train = vectorize_sequences(train_data)
# 我们的矢量化测试数据
x_test = vectorize_sequences(test_data)
print(len(x_train[0]),x_train.shape)
y_train = np.asarray(train_labels).astype('float32')
print(x_train.shape)
y_test = np.asarray(test_labels).astype('float32')#此处并没有向量化，只是进行数据类型转化
"""测试
s =[1,2,3,4,5,6]
s = vectorize_sequences(s)
print("测试结果如下：")
print(s)
"""

from keras import models
from keras import layers

model = models.Sequential()#一共三层
model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))#输入数据的数量
model.add(layers.Dense(16, activation='relu'))#activation使得线性变换得以扩展，走向非线性变换，以防无法处理非线性变换的问题
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',#交叉烱，求对数差，而均方误差求平方差
              metrics=['accuracy'])

#数据集划分
x_val = x_train[:10000]
partial_x_train = x_train[10000:]

y_val = y_train[:10000]
partial_y_train = y_train[10000:]

#训练
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=5,
                    batch_size=512,
                    validation_data=(x_val, y_val))#测试集

"""可视化"""
history_dict = history.history
print(history_dict.keys())
import matplotlib.pyplot as plt

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

"""损失下降图"""
# “ bo”代表“蓝点”
plt.plot(epochs, loss, 'bo', label='Training loss')
# b 用于“蓝色实线”
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

"""准确度图"""
plt.clf()   # clear figure
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

#依据两图确定轮次