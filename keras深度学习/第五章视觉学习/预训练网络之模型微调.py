"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""模型微调就是在冻结卷积基的基础上解封靠近顶层的卷积层"""
from keras import models,layers,optimizers
from keras.applications import VGG16
from keras.callbacks import ModelCheckpoint
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
#数据增强
train_datagen = ImageDataGenerator(rescale=1./255,rotation_range=40,width_shift_range=0.2,height_shift_range=0.2,
                                   shear_range=0.2,zoom_range=0.2,horizontal_flip=True,fill_mode='nearest')
test_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory( train_dir,target_size=(150, 150),batch_size=20,class_mode='binary')
#class_mode='binary'使得标签变为二进制
validation_generator = test_datagen.flow_from_directory(validation_dir,target_size=(150, 150), batch_size=20,class_mode='binary')


#可训练
conv_base.trainable = True
set_trainable = False
for layer in conv_base.layers:
    if layer.name == 'block5_conv1':#如果这样，不是只有block5_conv1比解封！！！！
        """非block5_conv1时，虽然conv_base.trainable可训练，但是layer.trainable=false即网络层禁止更新，而如果是则允许更新"""
        set_trainable = True
    if set_trainable:
        layer.trainable = True
    else:
        layer.trainable = False
filepath='J:\PyCharm项目\学习进行中\keras深度学习\model\cats_and_dogs_small_4_30epochs{epoch:02d}-{val_acc:.2f}.h5'
    # 有一次提升, 则覆盖一次.
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1,save_best_only=True,mode='max',period=2)
callbacks_list = [checkpoint]
model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=1e-5), metrics=['acc'])
history = model.fit_generator(train_generator, steps_per_epoch=100, epochs=30,validation_data=validation_generator,
      validation_steps=50,callbacks = callbacks_list)
#model.save('J:\PyCharm项目\学习进行中\keras深度学习\model\cats_and_dogs_small_4_30epochs.h5')

"""
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