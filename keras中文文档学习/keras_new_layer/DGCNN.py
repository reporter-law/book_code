# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
from keras.layers import *
import keras.backend as K
def Dilated_gated_conv1d(seq, mask, dilation_rate=1):
    """膨胀门卷积（残差式）
    """
    dim = K.int_shape(seq)[-1]    # size
    h = Conv1D(dim*2, 3, padding='same', dilation_rate=dilation_rate)(seq)   # (bs, sl, size*2)
    def _gate(x):
        dropout_rate = 0.1
        s, h = x   # (bs, sl, size)  (bs, sl, size*2)
        g, h = h[:, :, :dim], h[:, :, dim:]   #  (bs, sl, size)  (bs, sl, size)
        g = K.in_train_phase(K.dropout(g, dropout_rate), g)   # 训练中dropout
        g = K.sigmoid(g)   # (bs, sl, size)
        return g * s + (1 - g) * h
    seq = Lambda(_gate)([seq, h])
    seq = Lambda(lambda x: x[0] * x[1])([seq, mask])
    return seq
