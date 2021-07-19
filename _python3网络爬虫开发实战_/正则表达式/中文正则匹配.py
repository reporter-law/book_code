"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import re
path = r"C:\Users\lenovo\Desktop\新建文本文档.txt"
with open(path,"r")as f:
    content = f.read()
    print(re.findall(r'[\u4e00-\u9fa5]+', content))
    "中文和标点"
    print(re.findall(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]', content))
    #reg = '([\u96f6\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343\u4e07\u3007]+)年'中文数字+〇\u3007
