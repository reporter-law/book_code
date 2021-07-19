# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import requests
import  lxml
from  bs4 import BeautifulSoup

#url分析
'''url1 = 'https://www.jufaanli.com/search2?TypeKey=1%3A%E5%88%91%E4%BA%8B'

url2 ="https://www.jufaanli.com/search2?TypeKey=1:%E5%88%91%E4%BA%8B&Page=2"

url中page数量递增，但是后面可能需要账号登录'''
url = 'https://www.jufaanli.com/search2?TypeKey=1%3A%E5%88%91%E4%BA%8B+z%3Acase_level_1_%E6%99%AE%E9%80%9A%E6%A1%88%E4%BE%8B&search_uuid=b46172ce0f09aefa1cc52607589d6d82'

def get_page():
    try:
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        return r.text
    except:
        print('爬取失败')
        print(r.status_code)

def parse_page(html):
    soup = BeautifulSoup(html,'lxml')
    results = soup.find_all('div',attrs={'class':'jufa-search-list'})
    for result in results:
        ''''find_all()回来的是一个列表！！！！！'''
        print(results)
    #print('results' == '\u0061')
        tags = result.h3.span.a.find_all(class_='jufa-to-detail')
        for tag in tags:
            print(tag['href'])
def main():
    html = get_page()
    print(html)
    parse_page(html)
main()