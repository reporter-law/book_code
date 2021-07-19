# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
from pyquery import PyQuery
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

#def click_page():
ops = Options()
ops.binary_location = r'I:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
browser = webdriver.Chrome(options=ops)
browser.get('https://www.qidian.com/kehuan')
time.sleep(5)



click = browser.find_element_by_css_selector('div>a[href="//www.qidian.com/rank?chn=9"]')
print(click)

doc = PyQuery(url = 'https://www.qidian.com/kehuan')#省略了get和requests
#a = doc('a:nth-child(1)')
a = doc('a[href="//www.qidian.com/rank?chn=9"]')
a1 = doc('a[href]')
print(a)
print(a1)
#用不到
#下一级空格,属性不空格
#与xpath的区别在于有没有@，属性匹配一样、与属性提取不一样，
# 属性提取与beautifulsoup一样，因为都是css选择器，只是前者是attr,后者是attrs
#css最强大，bs4没有属性选择似乎？