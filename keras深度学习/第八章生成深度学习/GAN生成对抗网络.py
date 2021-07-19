# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os
#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import numpy as np
from keras.datasets import cifar10
from keras.models import Model
from keras.layers import Input,Dense,LeakyReLU,Reshape,Conv2D,Conv2DTranspose,Flatten,Dropout
from keras.optimizers import RMSprop
from keras.preprocessing import image
import os

latent_dim=32
# Cifar10图片尺寸
height,width=(32,32)
channels=3


# 生成网络：将隐空间中矢量生成图片，使用Conv2DTranspose
generator_input=Input((latent_dim,))
x=Dense(128*16*16)(generator_input)
# 只添加了一个alpha参数，其他地方跟书上一致，alpha默认0.3
x=LeakyReLU(alpha=0.1)(x)
x=Reshape((16,16,128))(x)
x=Conv2D(256,5,padding='same')(x)
x=LeakyReLU(alpha=0.1)(x)
# 结果为32*32*256，为避免生成图片呈现棋盘的点阵格式，凡是使用strides的地方，窗口大小为strides的整数倍
x=Conv2DTranspose(256,4,strides=2,padding='same')(x)
x=LeakyReLU(alpha=0.1)(x)

x=Conv2D(256,5,padding='same')(x)
x=LeakyReLU(alpha=0.1)(x)
x=Conv2D(256,5,padding='same')(x)
x=LeakyReLU(alpha=0.1)(x)

# 结果为32*32*3，即一个图片正确格式。使用tanh代替sigmoid
x=Conv2D(channels,7,activation='tanh',padding='same')(x)
generator=Model(generator_input,x)#它在包含在GAN里训练的，所以这里不用编译
# generator.summary()

# 鉴别网络
discriminator_input=Input((height,width,channels))
x=Conv2D(128,3)(discriminator_input)
x=LeakyReLU(alpha=0.1)(x)

x=Conv2D(128,4,strides=2)(x)
x=LeakyReLU(alpha=0.1)(x)
x=Conv2D(128,4,strides=2)(x)
x=LeakyReLU(alpha=0.1)(x)
# 2*2*128
x=Conv2D(128,4,strides=2)(x)
x=LeakyReLU(alpha=0.1)(x)
x=Flatten()(x)
# Dropout和给标签添加噪声，可以避免GAN卡住
x=Dropout(0.4)(x)
x=Dense(1,activation='sigmoid')(x)

discriminator=Model(discriminator_input,x)
# discriminator.summary()

# clipvalue，梯度超过这个值就截断，decay，衰减，使得训练稳定
discriminator_optimizer=RMSprop(lr=0.0003,clipvalue=1.0,decay=1e-8)
discriminator.compile(optimizer=discriminator_optimizer,loss='binary_crossentropy')

# 最后的生成对抗网络，由生成网络与对抗网络组合而成，此时冻结鉴别网络，训练的只是生成网络
discriminator.trainable=False
# 组成整个生成对抗网络
gan_input=Input((latent_dim,))
# 最终网络形式为鉴别网络作用于生成网络，故生成器也不用compile
gan_output=discriminator(generator(gan_input))
gan_optimizer=RMSprop(lr=0.0004,clipvalue=1.0,decay=1e-8)
gan=Model(gan_input,gan_output)
gan.compile(optimizer=gan_optimizer,loss='binary_crossentropy')

(x_train,y_train),(x_test,y_test)=cifar10.load_data()
# 选择frog类别，总共10个类
x_train=x_train[y_train.flatten()==6]
# reshape到输入格式 nums*height*width*channels，像素归一化
x_train=x_train.reshape((x_train.shape[0],)+(height,width,channels)).astype('float32')/255.
iters=10000
batch_size=20
save_dir=r'J:\PyCharm项目\学习进行中\keras深度学习\第八章生成深度学习\image\frog'

start=0
"""损失值t"""
for step in range(iters):
#     选取潜空间中随机矢量（正态分布）
    random_latent_vec=np.random.normal(size=(batch_size,latent_dim))
#     生成网络产生图片
    generated_images=generator.predict(random_latent_vec)
    stop=start+batch_size
#     真实原始图片
    real_images=x_train[start:stop]
#     mix生成和真实图片
    combined_images=np.concatenate([generated_images,real_images])
#     mix labels
    labels=np.concatenate([np.ones((batch_size,1)),np.zeros((batch_size,1))])
#     trick：标签添加随机噪声
    labels+=0.05*np.random.random(labels.shape)
#     鉴别loss，可能为负，因为使用的是LeakyReLU
    d_loss=discriminator.train_on_batch(combined_images,labels)
#     重新生成随机矢量
    random_latent_vec=np.random.normal(size=(batch_size,latent_dim))
    """故意设置标签为真实,目的就是纳入生成器训练中去"""
    misleading_targets=np.zeros((batch_size,1))
    a_loss=gan.train_on_batch(random_latent_vec,misleading_targets)
    start+=batch_size
    if start>len(x_train)-batch_size:
        start=0
    if step%100==0:
#         gan.save_weights('gan.h5')
        print('discriminator loss:',d_loss)
        print('adversarial loss:',a_loss)
#         保存一个batch里的第一个图片，之前像素归一化了，这里乘以255还原
        img=image.array_to_img(generated_images[0]*255.,scale=False)
        img.save(os.path.join(save_dir,'generated_frog'+str(step)+'.png'))
#         保存一个对比图片
        img=image.array_to_img(real_images[0]*255.,scale=False)
        img.save(os.path.join(save_dir,'real_frog'+str(step)+'.png'))
