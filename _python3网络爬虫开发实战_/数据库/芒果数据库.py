# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import pymongo
'''需要现行启动，因为设置手动启动'''
client = pymongo.MongoClient(host = 'localhost')
db = client.cnki
Collection = db.abstract
students = {'id':'27012300', 'name':'bob', 'age':21, 'gender':'male'}
result = Collection.insert_one(students)
print(result)#返回的是id值
results = Collection.find_one({'name':'bob'})
print(type(results))
print(results)
Collection.count_documents = Collection.count_documents
print(Collection.ount_documents)
result_1 = Collection.delete_one({'name':'bob'})
print(result_1)