"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

__browser_url = r'C:\Users\lenovo\AppData\Local\360Chrome\Chrome\Application\360chrome.exe'  ##360浏览器的地址
chrome_options = Options()

chrome_options.binary_location = __browser_url

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://wenshu.court.gov.cn/')

time.sleep(3)

driver.quit()
