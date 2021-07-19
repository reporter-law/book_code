# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
n_1 = int(input('一个整数： '))
n_2 = int(input('另一个整数： '))

if n_1 < n_2 :
    #n_2 = n_1
    '''需要保障n_2是两数之间的小数，不能直接赋，导致n_2这个原始大数没有了，
    下面就无法计算'''
    num = n_1
    n_1 = n_2
    n_2 = num

while n_2 != 0:
    num = n_1 % n_2
    n_1 = n_2
    n_2 = num
print(n_1)
'''思路保障n_2为小数，直到等于0'''
#问题1：之前的算法缺少输出

