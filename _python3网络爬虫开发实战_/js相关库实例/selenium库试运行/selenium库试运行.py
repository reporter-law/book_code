# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains
import selenium.webdriver.support.ui as ui

# 代理
"""
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.http', '211.142.247.153')
profile.set_preference('network.proxy.http_port', '4443')
profile.update_preferences()
"""
# 禁用浏览器缓存
"""
profile.set_preference("network.http.use-cache", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.sessionhistory.max_total_viewers", 3)
profile.set_preference("network.dns.disableIPv6", True)
profile.set_preference("Content.notify.interval", 750000)
profile.set_preference("content.notify.backoffcount", 3)
"""

browser = webdriver.Firefox()
#wait = ui.WebDriverWait(browser,100)
#browser.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
browser.implicitly_wait(0.1)
browser.get('https://www.bilibili.com/')
print(browser.get_cookies())
browser.delete_all_cookies()
print(browser.get_cookies())


#browser.get('https://www.zhihu.com/')
#print(browser.page_source)
input_one = browser.find_element_by_xpath('//*[@id="nav_searchform"]/input')
#input_two = browser.find_element(By.ID,'search-kw')
print(input_one)
#print(input_two)
input_one.send_keys('嵩天')
time.sleep(1)
#input_one.clear()
#input_one.send_keys('小米')
button = browser.find_element_by_xpath('//*[@id="nav_searchform"]/div/button')
button.click()
browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
browser.execute_script('alert("to botton")')#后面总说出错,可以但是不能一起用

time.sleep(100)
input = browser.find_element_by_xpath('//*[@id="app"]/div/a')
print(input.text)
'''browser.switch_to.frame('iframe')
source =browser.find_element_by_xpath('//*[@id="main"]/ul/li[1]/h3/a')#可能在iframe中
target = browser.find_element_by_id('droppable')
actions = ActionChains(browser)
actions.move_to_element(source)
#必须加上表单退出，否者就是死元素无法定位
self.browser.switch_to.default_content()
actions.perform'''
#time.sleep(10)
#browser.close()