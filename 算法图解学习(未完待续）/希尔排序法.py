# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:有大小使得插入次数减少
size = 8

def showdata(data):
    for i in range(size):
        print('%3d' %data[i], end='')
        print()

def shell(data,size):
    k=1
    m=1
    jmp=size//2
    while jmp != 0:
        for i in range(jmp, size):
            tem = data[i]
            no = i - jmp
            while no >= 0 and tem < data[no]:
                '''前一个数大于后一个数'''
                data[no + jmp] = data[no]  # 替代后一项，在原原列表的插入，但是没有使原列表数据消失，只是在增加
                no = no - jmp
                print('希尔一共%d次排序' %m)
                #简化了7次
                m+=1
            data[no + jmp] = tem
        print('这是第%d次排序' %k, end='')
        k+=1
        showdata(data)
        print('--------------------------------------------------------------------------')
        jmp=jmp//2
def main():
    data=[16, 25, 39, 27, 12, 8, 45, 63]
    print('原始数组：   ')
    showdata(data)
    print('--------------------------------------------------------------------------')
    shell(data,size)
main()
