# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from urllib.parse import quote
from scrapysplash.items import ScrapysplashItem
from scrapy_splash import SplashRequest #注意需要导入这个方法


script = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  for i=20,1,-1 
do 
   splash:evaljs('window.scrollTo(0,document.body.scrollHeight)')
   splash:wait(0.5) 
end
  return {
    html = splash:html(),
  }
end
"""



class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = 'http://www.zhihu.com/search?type=content&q='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORD'):
            url = self.start_urls + quote(keyword)
            yield SplashRequest(url = url, callback = self.parse,
                                endpoint = 'execute',args ={'lua_source':script})



    def parse(self, response):
        topics = response.xpath('//*[@id="SearchMain"]/div/div/div/div//div[@class="Card SearchResult-Card"]')

        for topic in topics:
            item = ScrapysplashItem()
            name = ''.join(topic.xpath('./div//span[@class="Highlight"]//text()').extract()).strip()
            item['name'] = name
            item['text'] = ''.join(topic.xpath('.//div/span[@class ="RichText ztext CopyrightRichText-richText"]//text()').extract()).strip()
            item['lable'] = ''.join(topic.xpath('.//span/button/@aria - label').extract()).strip()
            item['comment'] = ''.join(topic.xpath('.//button[@class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]/text()')
                                     .extract()).strip()
            yield item

