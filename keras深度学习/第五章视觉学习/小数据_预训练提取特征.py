"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os, shutil
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""预训练进行特征提取"""


"""数据预处理"""
def data_preprocessing():
    # 原始数据集路径
    original_dataset_dir = r'J:\PyCharm项目\学习进行中\keras深度学习\data\train\train'

    # 较小数据集的目录
    base_dir = r'J:\PyCharm项目\学习进行中\keras深度学习\data\cats_and_dogs_small'
    os.makedirs(base_dir)

    # 我们的训训，验证和测试拆分目录
    train_dir = os.path.join(base_dir, 'train')
    os.mkdir(train_dir)
    validation_dir = os.path.join(base_dir, 'validation')
    os.mkdir(validation_dir)
    test_dir = os.path.join(base_dir, 'test')
    os.mkdir(test_dir)

    # 猫图片
    train_cats_dir = os.path.join(train_dir, 'cats')
    os.mkdir(train_cats_dir)

    # 狗图片
    train_dogs_dir = os.path.join(train_dir, 'dogs')
    os.mkdir(train_dogs_dir)

    # 验证猫图片
    validation_cats_dir = os.path.join(validation_dir, 'cats')
    os.mkdir(validation_cats_dir)

    # 验证狗图片
    validation_dogs_dir = os.path.join(validation_dir, 'dogs')
    os.mkdir(validation_dogs_dir)

    # 测试猫图片
    test_cats_dir = os.path.join(test_dir, 'cats')
    os.mkdir(test_cats_dir)

    # 测试狗
    test_dogs_dir = os.path.join(test_dir, 'dogs')
    os.mkdir(test_dogs_dir)

    # 将前1000张猫图像复制到train_cats_dir
    fnames = ['cat.{}.jpg'.format(i) for i in range(1000)]
    for fname in fnames:
        src = os.path.join(original_dataset_dir, fname)
        dst = os.path.join(train_cats_dir, fname)
        shutil.copyfile(src, dst)

    # C将下500张猫图像复制到validation_cats_dir
    fnames = ['cat.{}.jpg'.format(i) for i in range(1000, 1500)]
    for fname in fnames:
        src = os.path.join(original_dataset_dir, fname)
        dst = os.path.join(validation_cats_dir, fname)
        shutil.copyfile(src, dst)

    # 将下500张猫图像复制到test_cats_dir
    fnames = ['cat.{}.jpg'.format(i) for i in range(1500, 2000)]
    for fname in fnames:
        src = os.path.join(original_dataset_dir, fname)
        dst = os.path.join(test_cats_dir, fname)
        shutil.copyfile(src, dst)

    # C将前1000张狗图像复制到train_dogs_dir
    fnames = ['dog.{}.jpg'.format(i) for i in range(1000)]
    for fname in fnames:
        src = os.path.join(original_dataset_dir, fname)
        dst = os.path.join(train_dogs_dir, fname)
        shutil.copyfile(src, dst)

    # 将下500张狗图像复制到validation_dogs_dir
    fnames = ['dog.{}.jpg'.format(i) for i in range(1000, 1500)]
    for fname in fnames:
        src = os.path.join(original_dataset_dir, fname)
        dst = os.path.join(validation_dogs_dir, fname)
        shutil.copyfile(src, dst)

    # 将下500张狗图像复制到test_dogs_dir
    fnames = ['dog.{}.jpg'.format(i) for i in range(1500, 2000)]
    for fname in fnames:
        src = os.path.join(original_dataset_dir, fname)
        dst = os.path.join(test_dogs_dir, fname)
        shutil.copyfile(src, dst)




"""数据展示"""
# 较小数据集的目录
base_dir = r'J:\PyCharm项目\学习进行中\keras深度学习\data\cats_and_dogs_small'
# 我们的训训，验证和测试拆分目录
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')
# 猫图片
train_cats_dir = os.path.join(train_dir, 'cats')
# 狗图片
train_dogs_dir = os.path.join(train_dir, 'dogs')
# 验证猫图片
validation_cats_dir = os.path.join(validation_dir, 'cats')
# 验证狗图片
validation_dogs_dir = os.path.join(validation_dir, 'dogs')
# 测试猫图片
test_cats_dir = os.path.join(test_dir, 'cats')
# 测试狗
test_dogs_dir = os.path.join(test_dir, 'dogs')
print('total training cat images:', len(os.listdir(train_cats_dir)))
print('total training dog images:', len(os.listdir(train_dogs_dir)))
print('total validation cat images:', len(os.listdir(validation_cats_dir)))
print('total validation dog images:', len(os.listdir(validation_dogs_dir)))
print('total test cat images:', len(os.listdir(test_cats_dir)))
print('total test dog images:', len(os.listdir(test_dogs_dir)))
#data_demonstration()

"""构建网络"""
from keras import layers
from keras import models

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',input_shape=(150, 150, 3)))#input_shape是随意的？？？
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
"""512应该是随机的，无所谓什么数？？？"""
model.add(layers.Dense(1, activation='sigmoid'))
#model.summary()
from keras import optimizers
model.compile(loss='binary_crossentropy',optimizer=optimizers.RMSprop(lr=1e-4),metrics=['acc'])#二元交叉熵

from keras.preprocessing.image import ImageDataGenerator#图像预处理函数

# 所有图像将按1./255重新缩放
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        # This is the target directory
        train_dir,
        # 图片将调整为150x150
        #"""这是之前输入特征图有效的原因"""
        target_size=(150, 150),
        batch_size=20,
        # 由于我们使用binary_crossentropy损失，因此我们需要二进制标签
        class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
        validation_dir,
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')
"""输入生成器数据的方法，steps_per_epoch=总数除以每轮生成器输出数据，总共训练集加验证集=2000，每轮20（batch_size=20,），故100轮"""
history = model.fit_generator(train_generator,steps_per_epoch=100,epochs=30,validation_data=validation_generator,
      validation_steps=50)
"""保存模型的方法"""
model.save('J:\PyCharm项目\学习进行中\keras深度学习\model\cats_and_dogs_small_1.h5')



"""绘图
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
