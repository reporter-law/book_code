# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:



'''形态figure-图类型(scatter)-具体值传入'''






from download_quick.download_quick import DownLoad_Module as d
from bokeh.plotting import  figure, show, output_file, ColumnDataSource
import sys


#print(help(ColumnDataSource))
'''自定义包的导入'''
sys.path.append(r'J:\\PyCharm项目\\学习进行中\\《python数据处理》\\第9章_数据探索和分析')
from 分离离群值 import highest_cpi_cl_rate as cpi
from bokeh.models import HoverTool
#标签属性说明



'''模块准备'''
def download_module():
    '''下载bokeh'''
    module = 'pyside'
    tm = d(module).download_module()
download_module()




'''外部图表figure的设置'''
TOOLS = "pan, reset, hover"
#工具栏 tools
# （2）移动、放大缩小、存储、刷新

def scatter_point(chart, x, y,source, marker_type ):
    '''图的一些参数传入'''
    chart.scatter(x, y, source = source,marker = marker_type,line_color="#6666ee",
                  fill_color = "#ee6666", fill_alpha=0.7,size=10)


'''图表外部的基本要素'''

chart = figure(title='Perceived Corruption and Child Labor in Africa', x_axis_label='CPI 2013 Score',tools=TOOLS)



'''图表输出路径'''
output_file("scatter_plot_.html")





'''值得传入'''

for row in cpi().rows:
    '''寻求x、y值的传入'''

    column_source = ColumnDataSource(
        data={'Country':[row['Country / Territory']]})
    #print(column_source)
    scatter_point(chart, float(row['CPI 2013 Score']),
                  float(row['Total (%) ']), column_source,'circle')


'''外部值设置的传入'''
hover = chart.select(dict(type=HoverTool))
hover.tooltips = [
    ("Country", "@Country"),
    ('CPI Score', "$x"),
    ("Child Labor (%)", "$y"),
]
#column_source可能是针对点的说明# 用于设置显示标签内容

show(chart)





