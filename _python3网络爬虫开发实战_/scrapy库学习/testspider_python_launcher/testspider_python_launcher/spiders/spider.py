# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['testspider.spider.com']
    start_urls = ['http://testspider.spider.com/']

    def parse(self, response):
        pass

    Fatal error in launcher: Unable to create process using '"c:\users\administrator\appdata\local\programs\python\python37\python.exe"  "D:\Users\Adminis
trator\AppData\Local\Programs\Python\Python37\Scripts\scrapy.exe" startproject spider': ???????????

