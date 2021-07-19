"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""rnn伪代码，设置一个处理量，不停的将现有量与处理量计算，然后将计算结果赋为处理量
i = 1
for i in range(t):
    b = a+i
    i = b
"""
import numpy as np

# 输入序列的时间步数
timesteps = 100
# 输入特征空间的维度
input_features = 32
# 输出特征空间的维度
output_features = 64

#输入数据：随机噪声
inputs = np.random.random((timesteps,input_features))

#初始状态：全零向量
state_t = np.zeros((output_features))

# 创建随机的权重矩阵
U = np.random.random((output_features,output_features))
W = np.random.random((output_features,input_features))
b = np.random.random((output_features,))

successive_outputs = []

for input_t in inputs: # input_t 是形状为 (input_features,) 的向量
    #由输入和当前状（前一个输出）计算得到当前输出
    output_t = np.tanh(np.dot(W,input_t)+np.dot(U,state_t)+b)
    #将这个输出保存到一个列表中
    successive_outputs.append(output_t)
    state_t = output_t

# 最终输出是一个形状为 (timesteps, output_features) 的二维张量
final_output_sequence = np.stack(successive_outputs, axis=0)
print(successive_outputs[2])
