# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import xlwt

wb = xlwt.Workbook()
ws = wb.add_sheet('信息')
for i in range(6):

    ws.write(i,0,'卡卡卡等')
    ws.write(i,1,'收到的')
    wb.save('dsd.xls')