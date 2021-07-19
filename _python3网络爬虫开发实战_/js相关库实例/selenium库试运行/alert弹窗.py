# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains
import selenium.webdriver.support.ui as ui


browser = webdriver.Firefox()

browser.implicitly_wait(0.1)
browser.get('https://www.bilibili.com/')
browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
browser.execute_script('alert("to botton")')