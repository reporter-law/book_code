# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os, warnings


def a(func):
    num = [0]

    def call_func():
        func()
        num[0] += 1
        print("执行次数为", num)

    return call_func
class ddd():
    def __init__(self):
        self.x = 1

    @a
    def man(self):
        for i in range(100):
            self.x +=1
print(ddd().man())

