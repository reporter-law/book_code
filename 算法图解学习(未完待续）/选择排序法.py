# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
# 收获：全文找大小

data = [9,5,1,3,7,6,4,8]
def select(data):
    for i in range(7):
        #print(i)#可以到7，所以不会有漏----到6
        '''i代表前一个，所以只有7位数，但是data一共八元素'''
        #print(i,end=' ')
        for j in range(i+1,8):
            #print(j)
            print(data[j],end=' ')
            print(data[8])
            '''data[8] IndexError: list index out of range,但是data[j]不会？？？？
            因为j不会到8，只会到7。总元素8，遍历只有7'''
            #print(j,end=' ')
            if data[i] > data[j]:
                data[i], data[j] = data[j], data[i]
    print('\n')
select(data)
for i in range(8):
    print(data[i],end=' ')