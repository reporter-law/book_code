#coding:gbk
import re

content = 'abcdcdajdhakjdhkh  ���132121564654987 ���'
#�����ַ�
r = re.search('.*?(���)', content)
print(r)
print(r.span())
#faindall �����б�������group�еĲ���group
a = [1,2,3]
print(len(a))