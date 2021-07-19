# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
from redis import StrictRedis
redis = StrictRedis(host = 'localhost',port=6379, db=1)
values = redis.randomkey()
print(redis.get())

