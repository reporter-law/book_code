"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:

import os

data_dir = r'J:\PyCharm项目\学习进行中\keras深度学习\data\气候数据'
fname = os.path.join(data_dir, 'jena_climate_2009_2016.csv')
f = open(fname)
data = f.read()
f.close()
lines = data.split('\n')
header = lines[0].split(',')
lines = lines[1:]

print(header)
# 数据解析
import numpy as np

float_data = np.zeros((len(lines), len(header) - 1))
"""塞入全0的张量中去"""
for i, line in enumerate(lines):
    values = [float(x) for x in line.split(',')[1:]]
    float_data[i, :] = values

"""数据准备：预处理缩放数据减去均值除以标准差"""
mean = float_data[:200000].mean(axis=0)
float_data -= mean
std = float_data[:200000].std(axis=0)
float_data /= std


#数据处理生成器，批量提取
def generator(data, lookback, delay, min_index, max_index,shuffle=False, batch_size=128, step=6):
    #min_index, max_index是怎样抽取数据的索引
    """data的格式为sample,data(时间，其它数据都在）"""
    if max_index is None:
        max_index = len(data) - delay - 1#delay为未来时间步数
    i = min_index + lookback#lookback为过去时间步数
    while 1:
        if shuffle:
            rows = np.random.randint(min_index + lookback, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            rows = np.arange(i, min(i + batch_size, max_index))
            #i是在记录并向下推移
            i += len(rows)

        samples = np.zeros((len(rows),lookback // step,data.shape[-1]))#//整数除法
        #print(samples.shape)#(128, 240, 14)240为十天，每个小时的数据量，14个检测数据
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][1]#
            """抽取时间数据"""
        yield samples, targets

# 先前已将其设置为6（每小时1点）。现在为3（每30分钟1分）。
step = 3
lookback = 720  # 原1440
delay = 144 #

train_gen = generator(float_data,
                      lookback=lookback,
                      delay=delay,
                      min_index=0,
                      max_index=200000,
                      shuffle=True,
                      step=step)
val_gen = generator(float_data,
                    lookback=lookback,
                    delay=delay,
                    min_index=200001,
                    max_index=300000,
                    step=step)
test_gen = generator(float_data,
                     lookback=lookback,
                     delay=delay,
                     min_index=300001,
                     max_index=None,
                     step=step)
val_steps = (300000 - 200001 - lookback) // 128
test_steps = (len(float_data) - 300001 - lookback) // 128

#模型
from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop
model = Sequential()
model.add(layers.Conv1D(32, 5, activation='relu',
                        input_shape=(None, float_data.shape[-1])))
model.add(layers.MaxPooling1D(3))
model.add(layers.Conv1D(32, 5, activation='relu'))#池化就是一中丢弃式的展平
"""可以直接搭rnn???????????,池化后就是二维张量"""
model.add(layers.GRU(32, dropout=0.1, recurrent_dropout=0.5))
model.add(layers.Dense(1))

model.summary()

model.compile(optimizer=RMSprop(), loss='mae')#RMSprop()微分平方加权平均数
history = model.fit_generator(train_gen,
                              steps_per_epoch=500,
                              epochs=8,
                              validation_data=val_gen,
                              validation_steps=val_steps)

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
