# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
import requests
from lxml import etree

url ='https://www.zhihu.com/topic/19552832/hot'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
r = requests.get(url,headers = headers)
print(r.status_code)

html = etree.HTML(r.text)
results = html.xpath('//*[@id="TopicMain"]/div[3]/div/div/div//text()')
for result in results:
    print(result)
