# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
# 收获：前后找大小，但是数据增加来找，优点不用遍历所有特别是在有序下
data = [9,5,1,3,7,6,4,8]
def show(data):
    '''打印数组'''
    for i in range(len(data)):
        print(data[i],end='')

def insert(data):
    '''核心算法'''
    m = 1
    for i in range(1,len(data)):
        '''第二个数'''
        tem = data[i]
        no = i - 1
        while no >=0 and tem<data[no]:
            '''前一个数大于后一个数'''
            data[no+1] = data[no]#替代后一项，在原原列表的插入，但是没有使原列表数据消失，只是在增加
            #print('这是第%d次排序' % no)
            print('这是第%d次排序' %m)
            m+=1

            print(show(data))
            print()

            no -= 1
            '''逆序，核心，将元素后推——注：存在两个循环，第二个循环保障大元素在后面，第一个循环保障原始元素不被篡改'''
        data[no+1] = tem
def main():
    print('原始数组：')
    print(show(data))
    insert(data)
    print('排序后数组: ')
    show(data)
main()

