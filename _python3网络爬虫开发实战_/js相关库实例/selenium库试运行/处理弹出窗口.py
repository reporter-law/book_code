# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
curHandle = browser.current_window_handle #获取当前窗口聚丙
allHandle = browser.window_handles #获取所有聚丙


"""循环判断，只要不是当前窗口聚丙，那么一定就是新弹出来的窗口，这个很好理解。"""
for h in allHandle:
        if h != curHandle:
            browser.switch_to.window(h) #切换聚丙，到新弹出的窗口




'''第二种弹窗'''
alert = browser.switch_to.alert
change = alert.text
print(change)
alert.accept()