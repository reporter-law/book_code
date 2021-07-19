# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import requests
data = {'q':'亚马逊'}
r = requests.get('https://hao.360.com/s',params = data)
print(r.status_code,r.request.url)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

try:
    r = requests.post('http://httpbin.org/post',data = data,headers=headers)
    print(r.status_code,r.request.url,r.cookies)
except:
    print('爬取失败')
"""除了构造参数，也可以直接在url中替换"""