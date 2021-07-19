# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
from mitmproxy import ctx
import json
import pymongo




def response(flow):
    ctx.log.warn(flow.request.url)
    for number in range(10):
        url = 'https://p.du.163.com/bookstore/module/more.json?moduleId=1001&entryId=410&page='+ str(number) +'&pageSize=102'
        response = flow.response
        info = ctx.log.info
        if flow.request.url.startswith(url):
            text = response.text
            data = json.loads(text)
            '''
            books = data.get('moreEntries')[0]
            book = books.get('book').get('title')
            info(str(book))
            这里的问题是需要str
            '''
            books = data.get('moreEntries')
        #info(str(books.get('book')))
        #info(str(books[0]))
            '''列表中是字典'''
            for book in books:
                data = {
                    'title' : str(book.get('book').get('title')),
                    'author':str(book.get('authors')[0].get('name')),#authors本身是一个列表，不能get只能序数
                    'description': str(book.get('book').get('description')),
                    'pubilisher':str(book.get('book').get('publisher')),
                    }
                info(str(data))
                save(data)
def save(data):
    client = pymongo.MongoClient('localhost')
    db = client['igetget']
    collection = db['books']
    if data:
        collection.insert(data)
    '''现在需要放进类里面才能够使用，需要在服务中先启动否则会出现目标计算机积极拒绝'''

#print(flow.request.url)
#出错地方1、request不是response,否则报错httpresponse attribute to url
'''其次，request需要flow在前'''
#print(response.text)