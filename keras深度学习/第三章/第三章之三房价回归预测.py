"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
from keras.datasets import boston_housing

(train_data, train_targets), (test_data, test_targets) =  boston_housing.load_data()
print(train_targets)#回归目标



#由于数据集差异大，因而需要进行数据处理，回想python机器学习中的数据预处理，标准化、放大缩小、方差等等
"""将全部取值范围大不相同的值输入到神经网络将是有问题的。网络也许能够自动适应这样的异构数据，但是肯定会使学习变得更加困难。
处理此类数据的最佳方法是按特征进行归一化：对于输入数据中的每个特征（输入数据矩阵中的一列），我们将减去特征的均值并除以标准差，
因此该特征将以0为中心，并具有单位标准偏差。这在Numpy中很容易做到："""
mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std
test_data -= mean
test_data /= std


from keras import models
from keras import layers

def build_model():
    # 因为我们将需要多次实例化同一模型，所以我们使用一个函数来构造它。
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu',
                           input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    """没有激活函数，这是一个线性层标量回归"""
    model.add(layers.Dense(1))#就是使得输出值不受限
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])#均方误差，检测绝对误差
    return model
#k折交叉验证
import numpy as np

k = 4
num_val_samples = len(train_data) // k
num_epochs = 500
all_scores = []
for i in range(k):
    print('processing fold #', i)
    #准备验证数据：来自分区k的数据
    val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
    """数据切片而已"""
    val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]

    # 准备训练数据：所有其他分区的数据
    partial_train_data = np.concatenate([train_data[:i * num_val_samples],train_data[(i + 1) * num_val_samples:]],axis=0)
    partial_train_targets = np.concatenate( [train_targets[:i * num_val_samples],train_targets[(i + 1) * num_val_samples:]],
        axis=0)

    # 建立Keras模型（已编译）
    model = build_model()#向上看
    history=model.fit(partial_train_data, partial_train_targets,epochs=num_epochs, batch_size=1)#verbose=0 静默即没有训练过程的显示
    #val_mse, val_mae = model.evaluate(val_data, val_targets, verbose=0)#Keras中model.evaluate（）返回的是 损失值和你选定的指标值（例如，精度accuracy）。
    mae_history = history.history['val_mean_absolute_error']#改为轮次的平均值
    all_mae_histories.append(mae_history)
#print(all_scores)
    #交叉验证的结果，返回cha'zhi差值的平方
import matplotlib.pyplot as plt

plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()


"""进行缩放"""
def smooth_curve(points, factor=0.9):
  smoothed_points = []
  for point in points:
    if smoothed_points:
      previous = smoothed_points[-1]
      smoothed_points.append(previous * factor + point * (1 - factor))
    else:
      smoothed_points.append(point)
  return smoothed_points

smooth_mae_history = smooth_curve(average_mae_history[10:])

plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()