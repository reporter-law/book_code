# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import requests
from lxml import etree
import requests
import re

class Login():
    def __init__(self):
        self.headers ={
            'content-type': 'application/json',
            'Upgrade - Insecure - Requests': '1',
            'Referer':'https://me.bdp.cn/login.html?lang=zh',
            'User-Agent' : 'Mozilla / 5.0(WindowsNT6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36',
            'Host' : 'me.bdp.cn',
            'Origin': 'https: // me.bdp.cn',
            'Sec - Fetch - Mode':'cors',
            'Sec - Fetch - Site': 'same - origin',
            }
        self.post_url = 'https://me.bdp.cn/api/user/login'
        '''错误原因该页面不是登录后的页面，登录后的页面是index即login选中后的页面，不是选中出错。在github中是session
        特点在，双击打开的就是登陆后的页面'''
        #self.post_url ='http://192.168.99.100:8050/render.html?url=https://me.bdp.cn/index.html'
        '''但是此处的问题在于没有表单，那就不知道有什么不一样了？'''
        self.logined_url = 'https://me.bdp.cn/index.html#/data_source'
        url = 'http://192.168.99.100:8050/render.html?url=https://me.bdp.cn/login.html?lang=zh'
        r = requests.get(url)
        html =r.text
        self.html = html
        self.session = requests.Session()

    def session_id_get(self):
        #获取动态session值
        session = etree.HTML(self.html)
        session_ids = session.xpath('//*[@id="login_box"]/div/div[1]/form/div[1]/div[2]/div[2]/div/img/@src')
        session_id = re.search('(\d+)',session_ids[0])
        #存在的问题是xpath出来的是list
        tokens = etree.HTML(self.html)
        token_ = tokens.xpath('/html/body/script[5]/text()')
        token__ = ''.join(token_)
        token = re.search(".*?token:(.*?),.*?",token__)

        '''不是session_id，'而是token,可能是这样！1'''
        return token.group(1),session_id.group(1)

    def login(self,username,password):
        post_data ={
            'domain': 'personal',
            'username': username,
            'session_id': self.session_id_get()[1],
            'token':self.session_id_get()[0],
            'password': password,
        }
        r = self.session.post(self.post_url,data = post_data,headers = self.headers)
        if r.status_code == 200:
            '''此处返回的是session'''
            print(r.text)
        else:
            print(r.status_code)
            '''已经登陆成功'''

            #self.dynamics(r.text)#只是输入的前提，接下来进行处理，定义def dynamics函数
            '''登陆页也有cookies，只是不是user_id开头'''
        r = self.session.get(self.logined_url,headers = self.headers)
        if r.status_code ==200:
            print(r.text)
            print(r.status_code)
            self.Profile(r.text)
            '''为什么出错？'''

    def Profile(self,html_):#html出现重复与self.html
        selector = etree.HTML(html_)
        origin = selector.xpath('//*[@id="J_dashEditView"]/div[1]/div/h2/text()')#多了一个中括号
        print(origin)

if __name__ == '__main__':
    ceshi = Login()
    ceshi.login(username='1063117365@qq.com',password = 'cao43100')
'''模拟登陆成功但是只有源码'''


#没有动态变化的东西，或者说这个就是验证码
'''没有找到问题看看是不是网址的问题'''
'''没有session_id时也可以'''
'''昨晚splash渲染不成功，可能是splash的原因'''#似乎不是splash的原因，每次渲染过去的都是登陆页面，需要execute进行交互操作？