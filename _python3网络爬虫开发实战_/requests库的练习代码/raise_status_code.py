# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import requests
#需要引号
try:
    r = requests.get('https://www.amazon.cn/dp/B07Y9C684P/ref=lp_116099071_1_12?s=books&ie=UTF8&qid=1583482910&sr=1-12')
    r.raise_for_status()
except:
    print('爬取失败')
print(r.status_code)
print(r.encoding)
r.encoding = r.apparent_encoding
#print(r.text)
print(r.encoding,r.request.headers)
headers = {'User-Agent':'Mozilla/5.0'}

try:
    r = requests.get('https://www.amazon.cn/dp/B07Y9C684P/ref=lp_116099071_1_12?s=books&ie=UTF8&qid=1583482910&sr=1-12',headers = headers)
    r.raise_for_status()
except:
    print('爬取失败')
print(r.encoding,r.request.headers, r.status_code,r.cookies)
for key,values in r.cookies.items():
    print('ok')
    print(key +'=' + values)
