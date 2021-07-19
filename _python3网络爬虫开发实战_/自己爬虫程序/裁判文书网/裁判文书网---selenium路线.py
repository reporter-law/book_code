# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait



driver = webdriver.Firefox()
wait = WebDriverWait(driver,10)
'''火狐可以正常打开，但是谷歌不行？'''
#无头化
#opt = webdriver.FirefoxOptions()
#opt.add_argument('--headless')
#driver = webdriver.Firefox(options = opt)
'''用options更好'''
url = 'http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=d0cfb3f1ce8e76a8a18797f87e15e00f&s8=02'
#url ='http://wenshu.court.gov.cn/website/wenshu/181107ANFZ0BXSK4/index.html?docId=b50177f2afdf459d9579ab8a011641a3'
driver.get(url)#需要加上https//*[@id="_view_1545184311000"]/div[3]/div[4]
button =  driver.find_element_by_xpath('/html/body/div/div[5]/div/div[2]/diy:lawyee/div/div[1]/div[3]')
#message = driver.find_element_by_xpath(('/html/body/div/div[5]/div/div[2]/diy:lawyee/div/div[1]/div[3]'))
#NamespaceError: An attempt was made to create or change an object in a way which is incorrect with regard to namespaces
#button = driver.find_element_by_xpath('')
button.click()


'''
input_one = browser.find_element_by_xpath('//*[@id="nav_searchform"]/input')
print(input_one)
input_one.send_keys('嵩天')

button = browser.find_element_by_xpath('//*[@id="nav_searchform"]/div/button')
button.click()
#browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
#browser.execute_script('alert("to botton")')#后面总说出错,可以但是不能一起用


input = browser.find_element_by_xpath('//*[@id="app"]/div/a')
print(input.text)
#time.sleep(10)
#browser.close()
'''