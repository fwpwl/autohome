# -*- coding: utf-8 -*-

import scrapy
import string
from getdetail import items
from scrapy.http import Request
import re


class ArticlesSpider(scrapy.Spider):
	name = "article"
	imgs = []
	start_urls = []
	# start_urls.append('https://www.autohome.com.cn/news/201802/912709.html#pvareaid=102624')
	start_urls.append('https://www.autohome.com.cn/all/2/')

	def parse_article(self, response):
		item = items.GetArticlesItem()
		info = response.meta['info']
		item['title'] = info['title']
		item['t_url'] = info['t_url']
		item['author'] = response.xpath('//div[@class="editor-select-wrap"]/a/text()').extract()[0]
		res = response.xpath('//div[@class="article-content"]//p')
		res_list = []
		for p in res[:-2]:
			tmp = {}
			if len(p.xpath('./a/img')) > 0:
				tmp['type'] = 'img'
				width = p.xpath('./a/img/@width').extract()[0]
				height = p.xpath('./a/img/@height').extract()[0]
				tmp['font'] = {'width': int(width), 'height': int(height)}
				url = 'http://cdn.autoforce.net/cyx/images/recommends/'
				self.imgs.append('https:' + p.xpath('./a/img/@src').extract()[0])
				tmp['url'] = url + p.xpath('./a/img/@src').extract()[0][2:].split('/')[-1]
			else:
				if len(p.xpath('./strong')) > 0:
					tmp['font'] = {'fontWeight': 'bold'}
				tmp['type'] = 'text'
				comment = p.xpath('string(.)').extract()[0]
				rv = re.findall(r'\u3000', comment)
				if len(rv) > 0:
					comment = re.sub('\u3000|\xa0', '   ', comment)
				if re.findall(r'『', comment):
					tmp['font'] = {'fontWeight': 'bold'}
					tmp['font']['marginBottom'] = 30
					tmp['font']['textAlign'] = 'center'
					rv = re.findall(r'\u3000', comment)
					if len(rv) > 0:
						comment = re.sub('\u3000|\xa0', '   ', comment)
				tmp['comment'] = comment
				print(tmp['comment'])
			res_list.append(tmp)
		item['comment'] = str(res_list)
		yield item

	def parse(self, response):
		res = response.xpath('//ul[@class="article"]/li')
		urls = []
		for k in res:
			info = {}
			if not k.xpath('.//a'):
				continue
			ems = k.xpath('.//em/text()').extract()
			url = 'https://' + k.xpath('.//a/@href')[0].extract()[2:]
			
			if ems:
				info['review_num'] = ems[0]
				info['comment_num'] = ems[1]
			info['t_url'] = k.xpath('.//div[@class="article-pic"]/img/@src').extract()[0][2:]
			info['title'] = k.xpath('.//h3/text()').extract()[0]
			print(info)
			info['url'] = url
			urls.append(info)
		for col in urls:
			yield Request(col['url'], meta={'info': col}, callback=self.parse_article)
