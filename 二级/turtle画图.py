"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import turtle,time
for i in range(4):
    turtle.fd(80)
    time.sleep(2)
    turtle.right(90)
#turtle.done()
def draw_snake():
    turtle.setup(1300,800,0,0)#画布
    turtle.pensize(30)#画笔宽度
    turtle.pencolor("blue")#画笔颜色
    turtle.seth(-40)#画笔角度逆时针
    for i in range(4):
        turtle.circle(40,80)#圆形轨迹爬行，rad半径，angle是弧度值
        time.sleep(2)
        turtle.circle(-40,80)
    turtle.circle(40,40)
    time.sleep(2)
    turtle.fd(40)#z直线爬行
    time.sleep(2)
    turtle.circle(16,180)
    turtle.fd(80/3)
#draw_snake()
