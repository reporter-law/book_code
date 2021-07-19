"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
#存储程序计算机：外部设备、cpu、内存
#程序语言：机器语言、汇编语言=机器加可读，高级语言
#编译语言：改为机器语言
"""IPO = INPUT,prohress,output"""
#列表操作：list.index()索引元素的索引，list.pop()依据索引删除元素
"""计算Π"""
def count_():
    import random
    from math import sqrt
    from time import clock
    clock()
    data = 12000000000
    hits = 0
    for i in range(1,data):
        x,y = random.random(),random.random()
        dist = sqrt(x**2+y**2)
        if dist < 1.0:
            hits = hits + 1
    pi =4*(hits/data)
    print(pi)
    print(clock())
#count_()
#if -elif -else为分支结构
#continue跳过本次循环，而break跳过循环
