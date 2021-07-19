# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
#函数本身进行自行调用

def function(i):
    if i == 1:
        return i
    else:
        ans = i * function(i-1)
        '''可以在内部自行调用自己，但是需要保留出口'''
        return  ans
print(function(1))
print(function(3))