"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
"""和lstm一样，都是在一致中随机化，保障全新相似而不一样"""
"""高维低维化，低维移动等于高维向量区域如微笑区域"""
import os

#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""图像转平均值与方差，随机采样后转为图像"""
import keras
from keras import layers
from keras import backend as K
from keras.models import Model
import numpy as np

img_shape = (28, 28, 1)
batch_size = 16
latent_dim = 2
"""潜在空间的维度：一个二维平面"""

input_img = keras.Input(shape=img_shape)

x = layers.Conv2D(32, 3, padding='same', activation='relu')(input_img)
x = layers.Conv2D(64, 3,padding='same', activation='relu',strides=(2, 2))(x)
x = layers.Conv2D(64, 3,padding='same', activation='relu')(x)
x = layers.Conv2D(64, 3,padding='same', activation='relu')(x)
shape_before_flattening = K.int_shape(x)

x = layers.Flatten()(x)
x = layers.Dense(32, activation='relu')(x)
"""输入图像变成z_mean,z_log_var,归一化为这两个参数"""
z_mean = layers.Dense(latent_dim)(x)
z_log_var = layers.Dense(latent_dim)(x)


def sampling(args):
    z_mean, z_log_var = args
    """计算epsilon随机数"""
    epsilon = K.random_normal(shape=(K.shape(z_mean)[0], latent_dim),mean=0., stddev=1.)
    """获得返回值采样的值"""
    return z_mean + K.exp(z_log_var) * epsilon

z = layers.Lambda(sampling)([z_mean, z_log_var])

# 这是我们将输入“ z”的输入。
decoder_input = layers.Input(K.int_shape(z)[1:])

"""#对输入进行上采样
#shape_before_flattening:(None,14,14,64)
#np.prod()函数用来计算所有元素的乘积:14*14*64
#获得上采样神经元的个数"""
x = layers.Dense(np.prod(shape_before_flattening[1:]),activation='relu')(decoder_input)
"""层反向转置"""
#重塑为与上一个“ Flatten”层之前的形状相同的图像
x = layers.Reshape(shape_before_flattening[1:])(x)

# 然后，我们将反操作应用于卷积层的初始堆栈：具有相应参数的`Conv2DTranspose`层
x = layers.Conv2DTranspose(32, 3,padding='same', activation='relu',strides=(2, 2))(x)
x = layers.Conv2D(1, 3,padding='same', activation='sigmoid')(x)
# 我们最终得到的特征图的大小与原始输入的大小相同。这是我们的解码器模型。
decoder = Model(decoder_input, x)

# 然后我们将其应用于`z`以恢复解码后的`z`。
z_decoded = decoder(z)
"""传统loss为loss(input,target)"""
"""vae自定义的loss，继承layer层"""
class CustomVariationalLayer(keras.layers.Layer):
    """定义loss函数"""
    def vae_loss(self, x, z_decoded):
        x = K.flatten(x)
        z_decoded = K.flatten(z_decoded)
        """一个是重构损失即新生成的损失i"""
        xent_loss = keras.metrics.binary_crossentropy(x, z_decoded)
        """正则化损失"""
        kl_loss = -5e-4 * K.mean(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
        #loss的平均计算
        return K.mean(xent_loss + kl_loss)
    """通过编写一个call方法来实现自定义层:层化"""
    def call(self, inputs):
        x = inputs[0]
        z_decoded = inputs[1]
        loss = self.vae_loss(x, z_decoded)
        self.add_loss(loss, inputs=inputs)
        """add_loss自定义损失函数层"""
        #我们不使用此输出。
        return x
y = CustomVariationalLayer()([input_img, z_decoded])
"""输入数值"""
from keras.datasets import mnist
"""Keras的函数式模型为Model，即广义的拥有输入和输出的模型，我们使用Model来初始化一个函数式模型;只是函数化可以调用"""
vae = Model(input_img, y)
"""优化器使得越来越小，正则化使得生成图像不会一样"""
vae.compile(optimizer='rmsprop', loss=None)
vae.summary()

# 用MNIST数字训练VAE
"""没有训练的y_train,,y为损失值，输入图像以loss为标签"""
(x_train, _), (x_test, y_test) = mnist.load_data()
"""数值归一化"""
x_train = x_train.astype('float32') / 255.
x_train = x_train.reshape(x_train.shape + (1,))
x_test = x_test.astype('float32') / 255.
x_test = x_test.reshape(x_test.shape + (1,))
"""使用自定义vae"""
vae.fit(x=x_train, y=None,shuffle=True,epochs=10, batch_size=batch_size,validation_data=(x_test, None))
# 我们在输入和解码的输出上调用自定义层，以获得最终的模型输出。


"""可视化"""
import matplotlib.pyplot as plt
from scipy.stats import norm

# 显示数字的二维流形
n = 15  # 15x15位数的数字
digit_size = 28
figure = np.zeros((digit_size * n, digit_size * n))
# 由于潜空间的先验是高斯，因此通过高斯的逆CDF（ppf）变换单位平方上的线性间隔坐标，以生成潜变量z的值。
grid_x = norm.ppf(np.linspace(0.05, 0.95, n))
grid_y = norm.ppf(np.linspace(0.05, 0.95, n))

for i, yi in enumerate(grid_x):
    for j, xi in enumerate(grid_y):
        z_sample = np.array([[xi, yi]])
        z_sample = np.tile(z_sample, batch_size).reshape(batch_size, 2)
        x_decoded = decoder.predict(z_sample, batch_size=batch_size)
        digit = x_decoded[0].reshape(digit_size, digit_size)
        figure[i * digit_size: (i + 1) * digit_size,
               j * digit_size: (j + 1) * digit_size] = digit

plt.figure(figsize=(10, 10))
plt.imshow(figure, cmap='Greys_r')
plt.show()