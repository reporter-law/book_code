# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import lxml
from lxml import etree
import requests
from tqdm import tqdm
import time
import json
import xlwt
from bs4 import BeautifulSoup

# url解析
# url分析 换页使得?offset=0的数字增加10
'''
def url_list():
    url_lists = []
    for number in tqdm(range(1)):
        url = 'https://maoyan.com/board/4?offset=' + str(number*10)
        url_lists.append(url)
    return url_lists'''


# 不知道搞什么一下行一下不行

# print(url_list())

# 网页返回
def page(url):
    # texts =[]
    # for url in url_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    r = requests.get(url, headers=headers)
    # texts.append(r.text)
    return r.text


# 内容解析 xpath实验
def content_one(html):
    soup = BeautifulSoup(html,'lxml')
    strs = soup.p.attrs['class']


    '''for items in content_lists:
        item_5 = items[5] + items[6]
        item = {'rank': items[0],
                'title': items[1],
                'img': items[2],
                'actor': re.sub('\s|n|\\\\', '', items[3]),  # 两个反斜杠去掉两个反斜杠
                'time': items[4],
                'core': item_5}
        content_list.append(item)'''
    return strs


# 一旦寻找顺序出错就会缺位，如img与title位置互换即title在前。


# print(content_one())
# 主演本身有空格
# core出现空‘’而没有评分是因为没有后界定符

def workhouse(item):
    with open('../../自己爬虫程序/movie_100.txt', 'a')as f:  # 用w不行，因为清楚之前，但是a可以后加,一个页面一个页面写入不能w
        f.write(json.dumps(item, ensure_ascii=False))
        f.close()


# 主函数
def main(number):
    url = 'https://maoyan.com/board/4?offset=' + str(number)
    html = page(url)
    print(content_one(html))  # 若不要workhouse导致只有最后10部电影，因为没有全部写入
    #workhouse(item)


if __name__ == '__main__':
    for i in tqdm(range(10)):
        main(number=i * 10)
        time.sleep(1)

# 注意：被给定的形参与下一个函数传递的形参需要一致才能够调用
#解析本地文件
def text_get():
    """bs4图片写入"""
    temp = r"C:\Users\lenovo\Desktop\法官量刑的限度：从危险驾驶罪的量刑情节影响因子谈起 -.html"
    html = open(temp,"r",encoding="gbk")
    htmlhandle = html.read()
    soup = BeautifulSoup(htmlhandle, 'lxml')
    print(soup)
    #print(len(content))


text_get()