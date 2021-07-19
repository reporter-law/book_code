#coding:gbk
import re

content = 'abcdcdajdhakjdhkh  早餐132121564654987 早餐'
#中文字符
r = re.search('.*?(早餐)', content)
print(r)
print(r.span())
#faindall 返回列表，本就是group中的不用group
a = [1,2,3]
print(len(a))