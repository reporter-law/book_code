# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
# 收获： 两两对比，前后找大小
data = [5,8,2,7,9,3,0,1,2]
for i in range(8):
    print('%3d'%data[i],end='')
    #print(data[i],end=' '),end是为了平行输出，%3d为占位符
print()
for i in range(7,-1,-1):#-1为通项即增减数值
    for j in range(i):
        if data[j] > data[j+1]:
            data[j], data[j+1] = data[j+1], data[j]
            '''此为核心，其余为格式,存在多次比较排序'''
    print('第%d次的排序结果为： ' %(8-i), end = '')
    for j in range(8):
        print('%3d' %data[j], end='')
    print()
print('排序后的结果为： ')
for i in range(8):
    print('%3d' %data[i],end='')

