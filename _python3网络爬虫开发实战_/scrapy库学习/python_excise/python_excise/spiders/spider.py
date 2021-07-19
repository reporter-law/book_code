# -*- coding: utf-8 -*-
import scrapy
from python_excise.items import PythonExciseItem
'''需要两次，多了一个目录！原因不知'''

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['quotes.toscrape.com']#域名
    start_urls = ['http://quotes.toscrape.com/']
    '''第一个为该文件名字，另一个为网址（可以任意）都可以'''

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = PythonExciseItem()
            item['text'] = quote.css('.text::text').extract_first()
            '''::text = .text(),extract()=find_all'''
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        next = response.css('.pager .next a::attr("href")').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url = url ,callback = self.parse)
        '''关键在Request,这个方法使得请求得以执行而与start_url无关，初始url也会请求，
                    这个方法在哪里没有关系，只要有Request'''
