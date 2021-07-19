"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import os,sys,math,time,random
#from crawler_tools import user_agent as u
from datetime import datetime
from selenium.common.exceptions import *
from retrying import retry
import pandas as pd

class Selenium_firefox():
    @retry(stop_max_attempt_number=3)
    def __init__(self):
        # 设置输出内容目录
        # 下载无弹窗
        self.casenames, self.caseurls, self.courts, self.casenumbers, self.times_, self.reasons = [],[],[],[],[],[]
        path = "F://firefox/Download"
        if not os.path.exists(path):
            os.makedirs(path)
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.dir', path.strip('\u202a'))
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip,application/octet-stream')
        # 无图
        profile.set_preference('browser.migration.version', 9001)
        profile.set_preference('permissions.default.image', 2)
        #无头
        ops = Options()
        ops.add_argument('--headless')
        ops.add_argument('disable-infobars')
        """网页获取"""
        self.browser = webdriver.Firefox(profile)
        self.wait = WebDriverWait(self.browser, 20,0.1)
        self.browser.get(
            'https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=3db4fb747da9705a88f1cbc0ee1e3287&s8=02')

    @retry(stop_max_attempt_number=3)
    def login(self):

        """登录"""
        # 切换框架
        self.browser.refresh()
        wait = self.wait
        frame = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contentIframe"]')))
        self.browser.switch_to.frame(frame)
        click = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#phoneNumber')))
        click.send_keys("18373281350")
        time.sleep(1)
        click1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.ng-invalid')))
        click1.send_keys("cao43100~")
        time.sleep(1)
        button_login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.custom-button')))
        button_login.click()
        time.sleep(1)
        # 必须加上表单退出，否者就是死元素无法定位
        self.browser.switch_to.default_content()
        click1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.advenced-search')))
        click1.click()

    def content_change(self,content):
        """主函数遍历页数"""
        # 当前目录下的城市限制调件
        keyword = content.strip().split(",")[0]
        wait =self.wait
        self.login()
        self.browser.refresh()
        """优化为发送country：高级检索 """
        click1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.advenced-search')))
        click1.click()
        send_ = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qbValue"]')))
        send_.clear()
        send_.send_keys(keyword)
        button_ = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchBtn"]')))
        button_.click()
        """文书数量：15"""
        button_ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pageSizeSelect > option:nth-child(3)')))
        button_.click()
        time.sleep(0.5)
        """目的：减少遍历次数，进行页数遍历"""
        condition = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_view_1545184311000"]/div[1]/div[2]/span')))
        conditions = math.ceil(int(condition.text) / 15)  # 最长12，最短6
        if conditions == 0:
            self.browser.close()
        elif int(conditions) > 40:  # condition本身已经除了15
            with open( './第三次超过600页.txt', 'a+', encoding='utf-8')as file:
                file.write( '出现超过600条的裁判文书,其所在区域为：' + str(country) + '，其数量为：' + str(condition.text) + str(keyword) + '\n')
        else:
            for index in range(conditions):
                pages = self.browser.find_elements_by_xpath('//*[@id="_view_1545184311000"]/div')
                pages = len(pages)
                print("一共%d篇裁判文书"%int(pages-3))
                for i in range(3,pages):
                    casename = self.browser.find_element_by_xpath(
                        f'//*[@id="_view_1545184311000"]/div[{i}]/div[2]/h4/a').text

                    self.casenames.append(casename)
                    caseurl = self.browser.find_element_by_xpath(
                        f'//*[@id="_view_1545184311000"]/div[{i}]/div[2]/h4/a').get_attribute("href")
                    self.caseurls.append(caseurl)
                    court = self.browser.find_element_by_xpath(
                        f'//*[@id="_view_1545184311000"]/div[{i}]/div[3]/span[1]').text
                    self.courts.append(court)
                    casenumber = self.browser.find_element_by_xpath(
                        f'//*[@id="_view_1545184311000"]/div[{i}]/div[3]/span[2]').text
                    self.casenumbers.append(casenumber)
                    times = self.browser.find_element_by_xpath(
                        f'//*[@id="_view_1545184311000"]/div[{i}]/div[3]/span[3]').text
                    self.times_.append(times)
                    reason = self.browser.find_element_by_xpath(
                        f'//*[@id="_view_1545184311000"]/div[{i}]/div[4]/p').text
                    self.reasons.append(reason)


                try:
                    '''全选的点击'''
                    time.sleep(1)
                    click_1 = wait.until(EC.element_to_be_clickable( (By.XPATH, '//div[@class="LM_tool clearfix"]/div[4]/a[1]/label')))
                    click_1.click()
                    '''批量下载的点击'''
                    click_2 = wait.until(EC.presence_of_element_located( (By.XPATH, '//html/body/div/div[4]/div[2]//div[@class="LM_tool clearfix"]/div[4]/a[3]')))
                    click_2.click()
                    print('{} 第{}页下载成功>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'.format(time.strftime('%Y{y}%m{m}%d{d}%H{h}%M{z}%S{s}').format(y='年', m='月', d='日',h="时",z="分",s="秒"),index))
                    """下一页的点击"""
                    button_ = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="left_7_3"]/a[last()]')))
                    button_.click()
                except:
                    print('第%d页可能出现缺失>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'%index)
        #self.browser.quit()
        path = os.path.dirname(__file__)
        with open(path + "./已经爬取的.txt", 'a', encoding='utf-8')as f:
            f.write(content+"\n")




    def main(self):
        # 读取限定词目录
        path = os.path.dirname(__file__)
        print(time.strftime('%Y{y}%m{m}%d{d}%H{h}%M{z}%S{s}').format(y='年', m='月', d='日', h="时", z="分",
                                                                     s="秒"))  # 转化的字符串中不能有中文
        file = path + r"/company1.txt"
        with open(file, 'r', encoding='utf-8')as f:
            contents = f.readlines()
        print("原contens", len(contents))
        file = path + r"/已经爬取的.txt"
        with open(file, 'r', encoding='utf-8')as f:
            del_contents = f.readlines()
        # 实现中断继续的功能
        contents = [i for i in contents if i not in del_contents]
        print("现在的contents", len(contents))

        for q in range(len(contents)):
            i = random.choice(contents)
            #print(i.strip("\ufeff"))
            self.content_change(i.strip("\n").strip("\ufeff"))
            print(self.casenumbers)
            contents.remove(i)
            self.browser.quit()

        message = {"案例名称": self.casenames,
                    "案例url": self.caseurls,
                    "法院": self.courts,
                    "案例号": self.casenumbers,
                    "判决日期": self.times_,
                    "裁判理由": self.reasons}
        print(message)
        dataframes = pd.DataFrame(message)
        output = os.path.dirname(__file__)
        writer = pd.ExcelWriter(output + r"/{name}案例详情.xls".format(name="ssss"))
        dataframes.to_excel(writer, sheet_name="aaaaaaa", index=False)
        writer.save()  #
        self.browser.quit()

if __name__ =="__main__":
    Selenium_firefox().main()





