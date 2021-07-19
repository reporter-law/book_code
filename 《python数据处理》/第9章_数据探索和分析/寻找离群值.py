# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获: 导入的函数需要加括号，同时离群值的寻找似乎除了问题，没有找到
from download_quick import download_quick as d
from 数据集连接再测试 import cpi_and_cl
import pprint


'''
安装准备库
module = 'agate-stats'
tm = d.DownLoad_Module(module)
tm.download_module()
'''
import agatestats
#agatestats.patch()
#print(help(agatestats))

print(cpi_and_cl().column_names)
def outlier():
    '''
    方差是各个数据与其算术平均数的离差平方和的平均数：整体离散程度、
    标准差，是各数据偏离平均数的距离的平均数，它是离均差平方和平均后的方根：每个数据的离散程度、
    离群值，会自动计算出标准差、方差不需要计算后形成表再使用该方法'''
    std_dev_outliers = cpi_and_cl().stdev_outliers('Total (%) ', deviations=3,reject=False)
    #deviations = 3是距离标准差的距离，越大越异常越离群
#pprint.pprint(std_dev_outliers.print_table(max_columns=30))
    print('离群值-------------------------------------------------------')
    for i in std_dev_outliers.rows:
        print(i['Country / Territory'],i['Total (%) '])
    print(len(std_dev_outliers))
    std_dev_outliers_ = cpi_and_cl().stdev_outliers('Total (%) ', deviations=5,reject=False)
    print(std_dev_outliers_)
    print(len(std_dev_outliers_))
'''语法正确，数据集出现问题,没有输出离群值'''




def average_outliers():
    '''平均绝对偏差：
    平均绝对误差是所有单个观测值与算术平均值的偏差的绝对值的平均。与平均误差相比，平均绝对误差由于离差被绝对值化，
    不会出现正负相抵消的情况，因而，平均绝对误差能更好地反映预测值误差的实际情况。
    '''
    print('平均绝对偏差-------------------------------------------------------')
    mad = cpi_and_cl().mad_outliers('Total (%) ')
    for i in mad.rows:
        print(i['Country / Territory'],i['Total (%) '])
average_outliers()

