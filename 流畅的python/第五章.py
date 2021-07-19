# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os, warnings
import random

"""函数是对象，即有身份的人，许多关联的东西能够用上去，如__doc__"""
def fun(n):
    """return n"""
    return n if n<2 else n*n-1
print(fun(42))
print(fun.__doc__)#输出解释

#any(),all()
"""任意元素是正值，所有数是正值"""

"""判断函数是否可以调用"""
a = lambda x:x+1
b = "c"
print(callable(a),callable(b))

"""类变成函数，使用__call__"""
class bingo():
    def __init__(self,item):
        self._item = list(item)
        random.shuffle(self._item)
    def pick(self):
        try:
            print( self._item.pop())
        except IndexError:
            raise LookupError("pick from empyter")
    def __call__(self):
        return self.pick()
a = bingo(range(10))
a.pick()
print(a)
print(callable(a))

"""不定参数"""
def fun(b,*args,a="2", **kwargs,):
    print("a:",a)
    print("b:",b)
    print('args=', args)
    print('kwargs=', kwargs)
print(fun(1, 2, 3, 4, A='a', B='b', C='c', D='d'))
print("*是元组，**是字典格式")
"""赋值参数需要元组不定参数后面，有赋值不捕获未命名参数，但是无则捕获"""