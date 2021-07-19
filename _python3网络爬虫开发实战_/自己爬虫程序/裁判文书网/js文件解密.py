# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
import execjs

# 读取js文件
with open('D:\\360极速浏览器下载\c3aqs9gktfr4.dfe1675.js', encoding='utf-8') as f:
    js = f.read()

# 通过compile命令转成一个js对象
docjs = execjs.compile(js)
print(docjs)
res = docjs.call('createGuid')
print(res)

# 调用变量
res = docjs.eval('guid')
print(res)


