# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from urllib.parse import quote
from scrapyseleniumtest.items import ScrapyseleniumtestItem


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = 'https://www.zhihu.com/search?type=content&q='
    '''注意此处为字符串'''

    def start_requests(self):
        for keyword in self.settings.get('KEYWORD'):
            url = self.start_urls + quote(keyword)
            yield Request(url = url, callback = self.parse, dont_filter=True)



    def parse(self, response):
        topics = response.xpath('//*[@id="SearchMain"]/div/div/div/div//div[@class="Card SearchResult-Card"]')
        #print(len(response.xpath('//div').extract()))
        #print(type(topics.extract()))
        print(len(topics.extract()))
        for topic in topics:
            print(type(topic.extract()))
            #print('测试——————————————————————————' + topic.extract())
            '''问题在于没有列表,只有一个元素'''
            #出现错误是因为xpath下来的是一个节点。节点后面是列表不等于节点是列表，节点不可遍历
            item = ScrapyseleniumtestItem()
            name = ''.join(topic.xpath('./div//span[@class="Highlight"]//text()').extract()).strip()
            #print(name)
            '''测试是否xpath 的 //会追诉topics'''
            #确实会追溯,用.就不会追溯

            name_1 =''.join(topic.css('.Highlight::text').extract()).strip()
            #name_1成功，不重复且也有
            '''extract()不能存在默认参数，但是extract_first()可以'''
            print(type(name))
            #print(name + '测试')#测试name,测试结果无name,诊断：xpath错误
            #问题2，name连在一起6遍，照理只有一遍，除非每次都有？topic是一个整块;诊断不是一整块;
            # 测试：xpath还是extract()的原因,诊断：不是exctact()的原因
            item['name'] = name

            '''没有也会重复'''
            item['text'] = ''.join(topic.xpath('.//div/span[@class ="RichText ztext CopyrightRichText-richText"]//text()').extract()).strip()
            item['lable'] = ''.join(topic.xpath('.//span/button/@aria - label').extract()).strip()
            item['comment'] = ''.join(topic.xpath('.//button[@class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]/text()')
                                     .extract()).strip()
            yield item
            '''问题：滚动不下去，索引难找'''
            #css选择器正确，xpath出现错误

