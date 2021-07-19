# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from scrapy.http import HtmlResponse
from logging import getLogger
import time


class SeleniumMiddleware():
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, timeout=None):#service_args=[]
        self.logger = getLogger(__name__)
        self.timeout = timeout
        #self.browser = webdriver.PhantomJS(service_args = service_args)
        opt = webdriver.ChromeOptions()
        opt.add_argument('--headless')

        self.browser = webdriver.Chrome(chrome_options = opt)#此处的options为chrome_options,否则报错
        self.browser.set_window_size(1400,700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser,self.timeout)
        '''测试：是否由于window——size'''
        '''只有一条数据，可能是botton[]序数限制'''
        #PhantomJS无法下滑，是不是PhantomJS的原因

    def __del__(self):
        self.browser.close()
    '''如果浏览器不关闭会不会滑到尾'''#不会

    def process_request(self, request, spider):
        self.logger.debug('PhantomJS is starting')#中间件的记录
        try:
            self.browser.get(request.url)
            '''input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Popover2-toggle"]'))
            )#xpath需要大写且没有selector
            button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/header/div[1]/div[1]/div/form/div/div/label/button'))
            )'''#不需要，因为没有页面
            #time.sleep(1)
            for i in range(10):
                self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            #for x in range(1,11):
                #j = x/10
                #js = "document.documentElement.scrollTop = document.documentElement.scrollHeight*%f"%j
                #self.browser.execute_script(js)
            #js也不好用
                time.sleep(1)
                '''基本齐全'''
            #self.browser.execute_script('alert("to botton")')
            #y原因selenium.common.exceptions.UnexpectedAlertPresentException: Alert Text: None
            #<super: <class 'WebDriverException'>, <UnexpectedAlertPresentException object>>

            return HtmlResponse(url = request.url, body = self.browser.page_source, request = request,
                                encoding = 'utf-8',status = 200)
        except TimeoutException:
            return HtmlResponse(url = request.url, status = 500, request = request)



    @classmethod
    def from_crawler(cls, crawler):
            # This method is used by Scrapy to create your spiders.
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
                   #service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))
