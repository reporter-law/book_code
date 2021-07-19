# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
from redis import StrictRedis

redis = StrictRedis(host = 'localhost',port=6379, db=0)#不用设置password，因为本地就没有设置
redis.set('name','bob')
print(redis.get('name'))
print(redis.exists('name'))
print(redis. dbsize())
