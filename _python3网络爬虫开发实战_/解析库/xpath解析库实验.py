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
"""要用self.wait.，要"fl-empty-table"双引号一致"""
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
    content_list = etree.HTML(html)
    #解析HTML文档，返回根节点对象  <Element html at 0x3c71588>
    #results = etree.tostring(content_list)   节点后面不是数字，也是英文字符
    #result  = results.decode('utf-8')#不用decode呈现机器编码是bytes即没有空格,decode只能解析成str即标准化
    '''总结：声明html格式化-tostring:获取全部文本-decode:标准化html'''
    #results = content_list.xpath('//*')获取网页中所有标签
    node_1 = content_list.xpath('//dd/i[@class]/text()')
    node_2 = content_list.xpath('//a/@title')#属性值

    #节点列表定位
    pages = page.xpath("/html/body/div[1]/div/div[3]/ul/li")
    for page in pages:
        text_url = page.xpath("h4/a/@href")  # 不需要/

    node_3 = content_list.xpath('//img/@data-src')
    node_4 = ' '.join(content_list.xpath('//p[@class="star"]/text()')).strip()#属性定位


    node_5 = content_list.xpath('//p[@class="releasetime"]/text()')
    node_6 = content_list.xpath('//i[@class="integer"]/text()')
    node_7 = content_list.xpath('//i[@class="fraction"]/text()')
    #/@属性返回属性值，【@属性=’‘】返回属性后的值，但是这之间没有/,总结：定位没有//，不定位就要//
    #text()、string()都会解码

    '''总结：当节点属性名称相同，那就找父节点定位区别，通过节点属性去寻找;向正则一样一次找出所有似乎不行'''

    '''for items in content_lists:
        item_5 = items[5] + items[6]
        item = {'rank': items[0],
                'title': items[1],
                'img': items[2],
                'actor': re.sub('\s|n|\\\\', '', items[3]),  # 两个反斜杠去掉两个反斜杠
                'time': items[4],
                'core': item_5}
        content_list.append(item)'''


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

