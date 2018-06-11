# -*- coding: utf-8 -*-

import scrapy
from getdetail import items


class CheZhuZhiJiaSpider(scrapy.Spider):
	name = "chezhuzhijia"
	start_urls = []
	for i in range(1, 1559):
		start_urls.append('http://dealer.16888.com/?tag=search&nature=3&page=%s'%i)
			
	def parse(self, response):
		item = items.CheZhuZhiJiaItem()
		item['url'] = response.url
		item['dtype'] = '4S店'
		# item['dtype'] = '综合店'
		# item['dtype'] = '平行进口'
		res = response.xpath('//dl[@class="clearfix hover last"]')
		res1 = response.xpath('//dl[@class="clearfix hover "]')
		res_list = res + res1
		for k in res_list:
			item['name'] = k.xpath('.//div[@class="title"]/a/text()').extract()[0]
			item['phone'] = k.xpath('.//div[@class="camp clearfix"]/em/text()').extract()[0]
			item['address'] = k.xpath('.//div[@class="camp clearfix"][2]/p/text()').extract()[0]
			yield item
