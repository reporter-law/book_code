# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import requests
url = 'http://192.168.99.100:8050/render.html?url=http://wenshu.court.gov.cn&wait=1'#将url放在splash中渲染一次，类网页再请求
r = requests.get(url)
#with open('wenshu.png','wb')as f:
    #f.write(r.content)
'''必须要等待时间，否则不成,不论是html还是png'''
print(r.text)