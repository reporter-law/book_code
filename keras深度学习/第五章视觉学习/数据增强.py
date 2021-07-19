"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
#加载数据集
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


"""数据增强就是利用现有数据生成新数据，包括角度变化、高宽拉伸、水平翻转等"""
from keras.preprocessing.image import ImageDataGenerator#图像预处理函数
from keras.preprocessing import image
"""
import matplotlib.pyplot as plt
datagen = ImageDataGenerator(rotation_range=80,width_shift_range=0.2,height_shift_range=0.2,shear_range=0.4, zoom_range=0.2,
      horizontal_flip=True, fill_mode='nearest')#使用最近的像素填充
'''# 宽度0.8会找不到猫！！
rotation_range是图像旋转
zoom_range：图像放大'''

# 这是带有图像预处理实用程序的模块

fnames = [os.path.join(train_cats_dir, fname) for fname in os.listdir(train_cats_dir)]
# 我们选择一张图片进行“增强”我们选择一张图片进行“增强”
img_path = fnames[3]
# 阅读图像并调整其大小
img = image.load_img(img_path, target_size=(150, 150))
# 将其转换为形状为（150、150、3）的Numpy数组
x = image.img_to_array(img)
# 将其重塑为（1，150，150，3）
x = x.reshape((1,) + x.shape)
# 下面的.flow（）命令生成一批随机变换的图像。它会无限循环，因此我们需要在某个时候“打破”循环！
开始数据增强即图像生成
i = 0
for batch in datagen.flow(x, batch_size=1):
    plt.figure(i)
    imgplot = plt.imshow(image.array_to_img(batch[0]))
    i += 1
    if i % 4 == 0:#一次四张
        break

plt.show()
"""

"""构建网络"""
from keras import layers
from keras import models
from keras import optimizers
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dropout(0.5))#dropout层随机丢弃
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])
train_datagen = ImageDataGenerator(rescale=1./255,
    rotation_range=80,
    width_shift_range=0.2,
    height_shift_range=0.4,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,)

# 请注意，不应增加验证数据！
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        train_dir,
        # All images will be resized to 150x150
        target_size=(150, 150),
        batch_size=32,
        # Since we use binary_crossentropy loss, we need binary labels
        class_mode='binary')

validation_generator = test_datagen.flow_from_directory(validation_dir,target_size=(150, 150),batch_size=32,class_mode='binary')

history = model.fit_generator(train_generator,steps_per_epoch=100, epochs=100,validation_data=validation_generator,
      validation_steps=50)
model.save('J:\PyCharm项目\学习进行中\keras深度学习\model\cats_and_dogs_small_2.h5')

"""绘图"""
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

