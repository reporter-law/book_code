"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""小型数据集训练：预训练网络"""
"""两种方法：特征提取、微调模型"""
"""特征提取，使用卷积基应该就是参数，不使用密集连接层在于其丢弃了空间信息，使用哪些卷积基取决于差异大不大，差异大选靠近底层的卷积基
"""
"""imagenet预训练网络层次:Xception、InceptionV3、ResNet50、VGG16、VGG19、MobileNet，前顶层后底层"""
"""卷积基使用方式，直接添加dense层，但是无法数据增强；顶部添加dense"""
from keras.applications import VGG16

conv_base = VGG16(weights='imagenet',include_top=False,input_shape=(150, 150, 3))#weights='imagenet'是导入imagenet vgg6的权重
#conv_base.summary()
"""非数据增强的卷积基使用"""
#数据导入
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

base_dir = 'J:\PyCharm项目\学习进行中\keras深度学习\data\cats_and_dogs_small'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')
#图像变换预处理
datagen = ImageDataGenerator(rescale=1./255)
batch_size = 20
def extract_features(directory, sample_count):
    """此为预训练输出的张量形状,目的是张量向量化？？？或是填充padding???"""
    features = np.zeros(shape=(sample_count, 4, 4, 512))
    labels = np.zeros(shape=(sample_count))
    """生成器处理时把图片变成了150，150"""
    generator = datagen.flow_from_directory(directory,target_size=(150, 150),batch_size=batch_size,class_mode='binary')
    i = 0
    for inputs_batch, labels_batch in generator:
        #print("图像预处理后的形状：",inputs_batch.shape)#(20, 150, 150, 3)20,图片数量，150为宽高，3为rgb通道
        features_batch = conv_base.predict(inputs_batch)
        #print("图像预训练后的形状：",features_batch.shape)#(20, 4, 4, 512)
        features[i * batch_size : (i + 1) * batch_size] = features_batch
        """用处理过的features代替原来的features,features生成的只是为0的张量空集"""
        labels[i * batch_size : (i + 1) * batch_size] = labels_batch
        i += 1
        #print("图像填充后的形状：", features)
        if i * batch_size >= sample_count:
            # 请注意，由于生成器无限循环地产生数据，因此必须在每个图像都被查看一次之后“中断”。
            break
    return features, labels

train_features, train_labels = extract_features(train_dir, 2000)
validation_features, validation_labels = extract_features(validation_dir, 1000)
test_features, test_labels = extract_features(test_dir, 1000)

#平整降维为一维，提取的特征当前具有形状（样本4、4、512）。我们将它们输入到一个紧密连接的分类器中，因此首先我们必须将它们展平为（样本，8192）：
train_features = np.reshape(train_features, (2000, 4 * 4 * 512))
validation_features = np.reshape(validation_features, (1000, 4 * 4 * 512))
test_features = np.reshape(test_features, (1000, 4 * 4 * 512))
"""小结逻辑：图片预处理为(20, 150, 150, 3)，然后预训练为(20, 4, 4, 512)，
然后将原来的features生成的只是为0的张量替换为预训练的张量，输入dense层中"""


"""开始dense层模型训练-特征提取下"""
from keras import models
from keras import layers
from keras import optimizers

model = models.Sequential()
model.add(layers.Dense(256, activation='relu', input_dim=4 * 4 * 512))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=optimizers.RMSprop(lr=2e-5), loss='binary_crossentropy', metrics=['acc'])

history = model.fit(train_features, train_labels,epochs=30,batch_size=20,validation_data=(validation_features, validation_labels))
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