"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
"""卷积层效果：
平移不变性即学习的边角可以在任何位置识别更加泛化---理由在于某些特征在此图这个位置可能在彼图另一个位置如近距离拍摄的图与远距离拍摄的图，
空间层次性即抓住细微，通道轴即颜色是任意的---黑白化"""
"""响应图：过滤器处理后的图（小图）；卷积核就是滤波器的值=小图与卷积核（权重矩阵）进行点积运算，输出1D张量，1d张量空间重组为输出特征图
填充即扩大图像，一般为0即无影响因为点积运算为0不影响系数；
最大池化：通常是2*2,步幅为2的滤波器，实质在于减少参数防止过拟合；
使用原因在于假定每个输入特征图在细微位置存在某种模式，最大池化可以提取这种模式
。如果不最大池化而是卷积核中使用步进可能使得细微提取不足而平均池化则可能无法提取细微特征！！！！！"""
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
from keras import layers
from keras import models

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))#32通道数也是卷积数，（3，3）是滤波器大小
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
"""平铺为1D向量，降维让dense层能够处理的张量"""
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

#数据处理
from keras.datasets import mnist
from keras.utils import to_categorical
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float32') / 255
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

#模型编译
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])#分类交叉熵
model.fit(train_images, train_labels, epochs=5, batch_size=64)
