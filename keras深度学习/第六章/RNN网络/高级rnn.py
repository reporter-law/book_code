"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os
#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""数值型数据处理"""
#数据读取

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
# 绘图
from matplotlib import pyplot as plt

"""第一个数值即为温度（摄氏度）"""

temp = float_data[:, 1]
plt.plot(range(len(temp)), temp)
plt.show()
print(temp[:1440])
plt.plot(range(1440), temp[:1440])
plt.show()
"绘图数据包括的多个点，只是将所有点都画出来了"
#read_data()
"""数据准备：预处理缩放数据减去均值除以标准差"""
mean = float_data[:200000].mean(axis=0)
float_data -= mean
std = float_data[:200000].std(axis=0)
float_data /= std

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
#训练
lookback = 1440#数据量一批次，为10天
step = 6 #取得是六个为一个训练数据的一组，即一小时数据量作为一组x
delay = 144
batch_size = 128#训练数据批量，一批数据中包含的样本数量称为batch_size
#min_index=0,max_index=200000为起始位置
train_gen = generator(float_data,lookback=lookback,delay=delay,min_index=0,max_index=200000,shuffle=True,step=step, batch_size=batch_size)
val_gen = generator(float_data,lookback=lookback,delay=delay,min_index=200001,max_index=300000,step=step,batch_size=batch_size)
test_gen = generator(float_data,lookback=lookback, delay=delay,min_index=300001,max_index=None,step=step,batch_size=batch_size)

# 这是从“ val_gen”绘制多少步骤才能看到整个验证集：
val_steps = (300000 - 200001 - lookback) // batch_size
# 这是从test_gen绘制多少步骤才能看到整个测试集的步骤：
test_steps = (len(float_data) - 300001 - lookback) // batch_size
'''
"""其实就是生成了多少次x,y数据集"""
#指标选择loss??
#np.mean(np.abs(preds - targets))
def evaluate_naive_method():
    batch_maes = []
    for step in range(val_steps):
        "next与迭代器一起使用，用于返回迭代器中的下一个迭代内容"
        samples, targets = next(val_gen)
        preds = samples[:, -1, 1]#最后一行的温度，tagert是未来的温度
        mae = np.mean(np.abs(preds - targets))
        batch_maes.append(mae)
    #print(np.mean(batch_maes))
    """对常识预测值求平均绝对误差就是loss的平均"""


evaluate_naive_method()


#编译模型
from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop

model = Sequential()
model.add(layers.Flatten(input_shape=(lookback // step, float_data.shape[-1])))
"""起到数据压平的作用，样本和数据集,原(128, 240, 14)压平没有关系，因为128本身就是批次"""
#print(lookback,float_data.shape[-1])#1440 14
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1))

model.compile(optimizer=RMSprop(), loss='mae')
"""这是以元组的形式传入数据"""
history = model.fit_generator(train_gen,
                              steps_per_epoch=500,
                              epochs=20,
                              validation_data=val_gen,
                              validation_steps=val_steps)#validation_steps = uniqueValidationData / batchSize   就是有多少批次数据
"""steps_per_epoch、validation_steps都是为了保障抽取数据集完全，多少只是影响数据集是否抽取完全，等于样本总量除以每个批次的样本量"""
#绘图
import matplotlib.pyplot as plt

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(loss))

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
'''
"""结论为不如常识有效，loss更大，大致在35%而常识为29%，原因复杂空间内无法找到简单问题的解决办法"""
"""layers.Flatten(input_shape=(lookback // step, float_data.shape[-1])消去的时间的概念，即依据一组一组数据与标签更加匹配，消去了组的概率也就使得预测无法落入组内"""
#使用rnn不展平
from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop

model = Sequential()
"""dropout需要报错一致，否者不利于"""
model.add(layers.GRU(32,dropout=0.2,recurrent_dropout=0.2, input_shape=(None, float_data.shape[-1])))
#指定每一时间步返回能够实现rnn的堆叠，方法为return_sequences=True

"""以小时组的概念输入"""
model.add(layers.Dense(1))

model.compile(optimizer=RMSprop(), loss='mae')
history = model.fit_generator(train_gen,steps_per_epoch=500,epochs=40,validation_data=val_gen,validation_steps=val_steps)


#绘图
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(loss))

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()

