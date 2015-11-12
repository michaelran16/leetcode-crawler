from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import Request

from leetcode_crawler.items import QuestionItem

import requests

# leetcode login
# username3
# password3
# email@email.com

class LeetcodeSpider(CrawlSpider):
    name = "leetcode"

    def start_requests(self):
        URL = "https://leetcode.com/problemset/algorithms/"
        # todo: did not do login here
        yield Request(URL, self.parse_list)

    def parse_list(self, response):
        # we check problem index range in here
        for trElement in response.xpath('//table[@id="problemList"]/tbody/tr'):
            # for each question, I get its ID and URL
            # ID might be checked against some predefined range, and also
            # IDs are passed to callback as a parameter, reason being taht 
            # the actually content page does not show a ID number.
            qIndex = trElement.xpath('td[2]/text()').extract()[0]
            qUrl = trElement.xpath('td[3]/a/@href').extract()[0]

            request = Request("https://leetcode.com" + qUrl, 
                            callback=self.parse_item)
            request.meta['qIndex'] = int(qIndex)
            yield request

    def parse_item(self, response):
        item = QuestionItem()

        item['index'] = str(response.meta['qIndex'])
        item['link'] = response.url
        item['content'] = response.xpath('//div[@class="question-content"]/*').extract()
        
        # there are somecases that page don't load when not logged in
        # omit these pages for now
        if not item['content']:
            return
        item['title'] = response.xpath('//div[@class="question-title"]/h3/text()').extract()[0]
        
        yield item
