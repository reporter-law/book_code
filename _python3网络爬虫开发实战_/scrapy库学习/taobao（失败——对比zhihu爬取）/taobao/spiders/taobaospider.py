# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from urllib.parse import quote
from taobao.items import TaobaoItem


class TaobaospiderSpider(Spider):
    name = 'taobaospider'
    allowed_domains = ['www.taobao.com']
    start_urls = 'https://www.taobao.com/search_product.htm?q='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORD'):
            for page in range(1,self.settings.get('MAX_PAGE')+1):
                url = self.start_urls + quote(keyword)#因为url相同
                yield Request(url=url, callback=self.parse, meta= {'page':page},dont_filter=True)

    def parse(self, response):
        products = response.xpath(
            '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class="item")]')
        print(type(products))
        for product in products:
            print(type(product))
            item =TaobaoItem ()
            item['price'] = ''.join(product.xpath('//div[contains(@class, "price")]//text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
            item['image'] = ''.join(
                product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
            item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
            item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
            yield item
