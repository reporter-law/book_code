"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""模型微调就是将预训练模型当成前面的层
在编译和训练模型之前，要做的一件非常重要的事情是冻结卷积基础。 “冻结”一层或一组层意味着防止其权重在训练期间更新。
如果我们不这样做，那么在训练过程中，卷积基础先前学习的表示形式将被修改。
由于顶部的密集层是随机初始化的，因此非常大的权重更新将通过网络传播，从而有效破坏了先前学习的表示形式。
原因就在于：反向传播误差即导数逆向传出，层与层之间也会互相传播从而整体改变系数
冻结卷积基础：使得数据不作张量变换

使用此设置，仅训练来自我们添加的两个密集层的权重。总共有四个权重张量：每层两个（主要权重矩阵和偏置）。
请注意，为了使这些更改生效，我们必须首先编译模型。如果在编译后修改了权重训练性，则应重新编译模型，否则这些更改将被忽略。
即在model.compile前
"""
from keras import models,layers,optimizers
from keras.applications import VGG16
"""预训练模型"""
conv_base = VGG16(weights='imagenet',include_top=False,input_shape=(150, 150, 3))#weights='imagenet'是导入imagenet vgg6的权重
#数据导入
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

base_dir = 'J:\PyCharm项目\学习进行中\keras深度学习\data\cats_and_dogs_small'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')


"""模型重新训练"""
model = models.Sequential()

model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
print('冻结之前可训练的张量个数:', len(model.trainable_weights))
conv_base.trainable = False#张量冻结，使得后面的dense层导数不逆向改变原权重
"""测试：与位置没有关系，不能在model.compile下面，导致info ops"""
print('冻结之后可训练的张量个数:', len(model.trainable_weights))


#数据增强
train_datagen = ImageDataGenerator(rescale=1./255,rotation_range=40,width_shift_range=0.2,height_shift_range=0.2,
                                   shear_range=0.2,zoom_range=0.2,horizontal_flip=True,fill_mode='nearest')
test_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory( train_dir,target_size=(150, 150),batch_size=20,class_mode='binary')
#class_mode='binary'使得标签变为二进制
validation_generator = test_datagen.flow_from_directory(validation_dir,target_size=(150, 150), batch_size=20,class_mode='binary')

"""模型编译"""
model.compile(loss='binary_crossentropy',optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])

history = model.fit_generator( train_generator,steps_per_epoch=100,epochs=30,validation_data=validation_generator,
                               validation_steps=50)
model.save('J:\PyCharm项目\学习进行中\keras深度学习\model\cats_and_dogs_small_3.h5')
"""
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
"""