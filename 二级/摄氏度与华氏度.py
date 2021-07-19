"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:、

def change():
    #摄氏度与华氏度的转化
    val = input("输入摄氏稳定或者华氏温度，摄氏度如23c,华氏度如34F\n")
    if val[-1] == "F" or val[-1] == "f":
        print(f"摄氏稳定为：{int(int(val[:-1])- 32)/1.8 }")
    elif val[-1] == "C" or val[-1] == "c":
        print(f"华氏温度为：{int(val[:-1])*1.8 + 32}")
    else:
        print("输入错误")
change()

