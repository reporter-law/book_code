# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os, warnings

warnings.filterwarnings("ignore")
def data_generate(lis):
    #准备工作，输入lis为二维张量，[[x_train,y_train],
     #                           [x_train, y_train],
    #                              ...]
    #y_train为可以直接输入的数据，即one-hot编码过了
    #注意训练为model.fit_generator，第一层需要填入input_shape,最后一层需要num_class即标签种类要确定填入
    count=1
    batch_size = 10
    while 1:
        batch_x = [x[0] for x in lis[(count - 1) * batch_size:count * batch_size]]
        batch_y = [y[1] for y in lis[(count - 1) * batch_size:count * batch_size]]
        batch_x = np.array([np.asarray(get_wav_mfcc(i)) for i in batch_x])
        batch_y =np.array(batch_y)
        count = count + 1
        yield batch_x, batch_y

