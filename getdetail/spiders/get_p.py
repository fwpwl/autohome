# -*- coding: utf-8 -*-

import scrapy
from getdetail import items
import logging
import string


class PinPaiSpiders(scrapy.Spider):
	name = 'p'
	start_urls=[]
	for a in string.ascii_uppercase:
		url = ('http://www.autohome.com.cn/grade/carhtml/%s.html' % a)
		start_urls.append(url)
		
	def parse(self, response):
		item = items.PinPaiItem()
		res = response.xpath('//body/dl/dd/ul')
		for i in res:
			name = i.xpath('./preceding-sibling::*/text()').extract()[-1]
			ids = i.xpath('./li/@id').extract()
			for id in ids:
				id = id[1:]
				item['series_id'] = id
				item['series_name'] = name
				yield item