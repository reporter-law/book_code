"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:打扰数据、，时间预测时不用打乱数据、确保数据训练集与测试集没有交集
"""数据预处理：向量化、值标准化（取值在0-1之间、取值范围大致相同、标准化x-=x.mean(axis=0),x/=x.std(axis=0)\缺失值可以设为0"""
"""深度学习的关键在于泛化，因为也容易优化"""
"""通用工作流程：定义问题收集数据，-确定问题如分类问题还是回归问题-注意非平稳问题即周期性但你在周期内数据进行预测-评估指标：
数据集平衡auc,数据集不平衡recall--数据格式化为张量、缩放预处理、特征工程"""
#l1,l2惩戒（l2即权重衰减，l1为绝对值、l2为系数平方
kernel_regularizer=regularizers.l2(0.001)#l2惩戒、系数为0.001
kernel_regularizer=regularizers.l1(0.001)
model.add(layers.Dropout(0.5))#添加dropout正则化层，丢弃率50%
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
