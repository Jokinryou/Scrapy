# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from autohome.items import AutohomeItem

import chardet

class AutohomeSpider(BaseSpider):
    name = "autohome"
    allowed_domains = ["autohome.com.cn"]

    start_urls = [
            "http://www.autohome.com.cn/list/c70-1.html"
            ]

    def parse(self, response):
        items = []
        hxs = HtmlXPathSelector(response)

        encoding = chardet.detect(response.body)['encoding']
        print encoding
        if encoding != 'utf-8':
            response.body = response.body.decode(encoding,'replace').encode('utf-8')

        #通过XPath选出新闻页面的URL
        cat_urls = hxs.select('//html/body/div/div[3]/div[2]/div[2]/div/span[2]/a/@href').extract()
        print 'cat_urls = ', cat_urls
        for url in cat_urls:
            item = AutohomeItem()
            item['link'] = url
            items.append(item)
        for item in items:
            yield Request(item['link'],meta={'item':item},callback=self.parse_content)

    def parse_content(self, response):
        encoding = chardet.detect(response.body)['encoding']
        print encoding
        if encoding != 'utf-8':
            response.body = response.body.decode(encoding,'replace').encode('utf-8')

        hxs = HtmlXPathSelector(response)
        content = hxs.select('//html/body/div[4]/div[4]/div/div')

        contents = hxs.select('//div[@class="article"]')
        item = AutohomeItem()
        for content in contents:
            item['title'] = content.select('h1/text()').extract()
            item['date'] = content.select('div[@class="article_info"]/span[1]/text()').extract()
            item['content'] = content.select('div[@class="article_con"]/p/text()|div[@class="article_con"]/p/a/text()').extract()
        return item

        #item = AutohomeItem()
        #item['title'] = content.select('h1/text()').extract()
        #item['date'] = content.select('div/span/text').extract()
        #item['content'] = content.select('div[3]/p/text()').extract()

        return item
