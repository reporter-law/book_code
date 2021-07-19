# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re


#关键在offset,成20递增
#共有内容  https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=80&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis
# ?aid=24&app_name=web_search&
# offset=80
# &format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20
# &en_qc=1&cur_tab=1&from=search_tab&pd=synthesis
#构造url
url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=80&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis'
def get_page(offset):
    parms ={
        #'aid':'24',加上返回none,aid为栏目代码！
        'app_name':'web_search',
        'offset': offset,
        'format':'json',
        'keyword' : '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc':'1',
        'cur_tab':'1',
        'from':'search_tab',
        'pd':'synthesis'
    }
    url ='https://www.toutiao.com/api/search/content/?'+ urlencode(parms)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    try:
        r = requests.get(url,headers=headers,timeout = 10)#requests没有parms
        r.raise_for_status()
        return r.json()
    except:
        print('爬取失败')
        print(r.status_code)

#print(get_page(20))
def get_htmlcontent(json):
    if json.get('data'):
        print(json.get('data'))#data里面有title
        for item in json.get('data'):#遍历此页的街拍
            title = item.get('title')
            #为什么是title，而不是abstract
            images = item.get('image_list')
            if images:
                for image in images:
                    yield {#yield相当于return,但是只返回一次的return，返回之后就没有了，再次调用这个函数也没有返回内容了。用return也行只是速度变慢
                        'image':image.get('url'),#此处的url是引号的，因为通过键获取的值
                        'title':title
                    }

def save_images(item):
    if not os.path.exists(item.get('title')):
        #r = re.sub('\s','', item.get('title'))

        os.makedirs(os.path.abspath(os.path.dirname(__file__))+"\\"+item.get('title'))#创建的是同级目录
        #mkdir为创造一个目录,makedirs()还是不行,指定路径也不行,增加str(),因为出现文件名不对！
    try:
        r = requests.get(item.get('image'))#因为通过键值对获得值
        r.raise_for_status()
        file_path = os.path.abspath(os.path.dirname(__file__))+'{0}/{1}.{2}'.format(item.get('title'), md5(r.content).hexdigest(), 'jpg')
        #前面是占位，后为格式
        #/前为目录
        if not os.path.exists(file_path):
            #os.makedirs(item.get('title'))
            with open(file_path, 'wb')as f:#出现filenotfound!!
                f.write(r.content)
        else:
            print('Already Download', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

def main(offset):
    json = get_page(offset)
    for item in get_htmlcontent(json):
        #print(item)
        save_images(item)

GROUP_START = 1
GROUP_END = 20
if __name__ == '__main__':
    pool = Pool()
    group = ([x*20 for x in range(GROUP_START, GROUP_END + 1)])#process中的group基本不用，但这个不是process，但是这个不是
    pool.map(main,group)#即一次性发起了20个请求，其中的group相当于赋值即付给main的值
    '''然而offset为偏离值，20、40、60，其中已经乘了20，'''
    pool.close()
    pool.join()

#1、可以对函数进行遍历以给第二个函数使用

