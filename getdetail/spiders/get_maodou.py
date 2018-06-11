# -*- coding: utf-8 -*-

import scrapy
import string
from getdetail import items
import logging
from scrapy.http import Request
import json
import pymysql.cursors
from selenium import webdriver
from bs4 import BeautifulSoup
import re


class MaodouSpider(scrapy.Spider):
	def __init__(self):
		self.driver = webdriver.PhantomJS()
	name = "maodou"
	start_urls = ['https://www.maodou.com/www/fyc/brifinfo/CfC', 'https://www.maodou.com/www/fyc/brifinfo/CeC', 'https://www.maodou.com/www/fyc/brifinfo/3VC', 'https://www.maodou.com/www/fyc/brifinfo/3UC', 'https://www.maodou.com/www/fyc/brifinfo/3wC', 'https://www.maodou.com/www/fyc/brifinfo/3mC', 'https://www.maodou.com/www/fyc/brifinfo/3iC', 'https://www.maodou.com/www/fyc/brifinfo/CcC', 'https://www.maodou.com/www/fyc/brifinfo/3AC', 'https://www.maodou.com/www/fyc/brifinfo/3LC', 'https://www.maodou.com/www/fyc/brifinfo/w1C', 'https://www.maodou.com/www/fyc/brifinfo/CSC', 'https://www.maodou.com/www/fyc/brifinfo/CFC', 'https://www.maodou.com/www/fyc/brifinfo/COC', 'https://www.maodou.com/www/fyc/brifinfo/34C','https://www.maodou.com/www/fyc/brifinfo/3PC', 'https://www.maodou.com/www/fyc/brifinfo/3hC', 'https://www.maodou.com/www/fyc/brifinfo/w6C', 'https://www.maodou.com/www/fyc/brifinfo/wCC', 'https://www.maodou.com/www/fyc/brifinfo/wUC', 'https://www.maodou.com/www/fyc/brifinfo/wYC', 'https://www.maodou.com/www/fyc/brifinfo/wNC', 'https://www.maodou.com/www/fyc/brifinfo/wQC', 'https://www.maodou.com/www/fyc/brifinfo/wLC', 'https://www.maodou.com/www/fyc/brifinfo/wcC', 'https://www.maodou.com/www/fyc/brifinfo/CYC', 'https://www.maodou.com/www/fyc/brifinfo/yVC', 'https://www.maodou.com/www/fyc/brifinfo/yLC', 'https://www.maodou.com/www/fyc/brifinfo/yMC', 'https://www.maodou.com/www/fyc/brifinfo/yiC','https://www.maodou.com/www/fyc/brifinfo/ylC', 'https://www.maodou.com/www/fyc/brifinfo/yEC', 'https://www.maodou.com/www/fyc/brifinfo/ykC', 'https://www.maodou.com/www/fyc/brifinfo/yhC', 'https://www.maodou.com/www/fyc/brifinfo/wZC', 'https://www.maodou.com/www/fyc/brifinfo/3oC', 'https://www.maodou.com/www/fyc/brifinfo/w0C', 'https://www.maodou.com/www/fyc/brifinfo/3CC', 'https://www.maodou.com/www/fyc/brifinfo/yfC', 'https://www.maodou.com/www/fyc/brifinfo/3FC', 'https://www.maodou.com/www/fyc/brifinfo/3sC', 'https://www.maodou.com/www/fyc/brifinfo/yAC', 'https://www.maodou.com/www/fyc/brifinfo/yeC', 'https://www.maodou.com/www/fyc/brifinfo/36C', 'https://www.maodou.com/www/fyc/brifinfo/38C','https://www.maodou.com/www/fyc/brifinfo/yBC', 'https://www.maodou.com/www/fyc/brifinfo/y4C', 'https://www.maodou.com/www/fyc/brifinfo/yPC', 'https://www.maodou.com/www/fyc/brifinfo/3OC', 'https://www.maodou.com/www/fyc/brifinfo/CsC', 'https://www.maodou.com/www/fyc/brifinfo/3XC', 'https://www.maodou.com/www/fyc/brifinfo/32C', 'https://www.maodou.com/www/fyc/brifinfo/30C', 'https://www.maodou.com/www/fyc/brifinfo/3RC', 'https://www.maodou.com/www/fyc/brifinfo/31C', 'https://www.maodou.com/www/fyc/brifinfo/3qC', 'https://www.maodou.com/www/fyc/brifinfo/3rC', 'https://www.maodou.com/www/fyc/brifinfo/3vC', 'https://www.maodou.com/www/fyc/brifinfo/3bC', 'https://www.maodou.com/www/fyc/brifinfo/ywC','https://www.maodou.com/www/fyc/brifinfo/3GC', 'https://www.maodou.com/www/fyc/brifinfo/3pC', 'https://www.maodou.com/www/fyc/brifinfo/3KC', 'https://www.maodou.com/www/fyc/brifinfo/39C', 'https://www.maodou.com/www/fyc/brifinfo/3aC', 'https://www.maodou.com/www/fyc/brifinfo/CZC', 'https://www.maodou.com/www/fyc/brifinfo/CHC', 'https://www.maodou.com/www/fyc/brifinfo/C6C', 'https://www.maodou.com/www/fyc/brifinfo/CrC', 'https://www.maodou.com/www/fyc/brifinfo/CKC', 'https://www.maodou.com/www/fyc/brifinfo/CbC', 'https://www.maodou.com/www/fyc/brifinfo/wHC', 'https://www.maodou.com/www/fyc/brifinfo/waC', 'https://www.maodou.com/www/fyc/brifinfo/CmC', 'https://www.maodou.com/www/fyc/brifinfo/CoC','https://www.maodou.com/www/fyc/brifinfo/CGC', 'https://www.maodou.com/www/fyc/brifinfo/CJC', 'https://www.maodou.com/www/fyc/brifinfo/CaC', 'https://www.maodou.com/www/fyc/brifinfo/w9C', 'https://www.maodou.com/www/fyc/brifinfo/CdC', 'https://www.maodou.com/www/fyc/brifinfo/wvC', 'https://www.maodou.com/www/fyc/brifinfo/wVC', 'https://www.maodou.com/www/fyc/brifinfo/wEC', 'https://www.maodou.com/www/fyc/brifinfo/wjC', 'https://www.maodou.com/www/fyc/brifinfo/wlC', 'https://www.maodou.com/www/fyc/brifinfo/35C', 'https://www.maodou.com/www/fyc/brifinfo/3cC', 'https://www.maodou.com/www/fyc/brifinfo/3uC', 'https://www.maodou.com/www/fyc/brifinfo/3nC', 'https://www.maodou.com/www/fyc/brifinfo/CIC','https://www.maodou.com/www/fyc/brifinfo/CWC', 'https://www.maodou.com/www/fyc/brifinfo/3dC', 'https://www.maodou.com/www/fyc/brifinfo/3eC', 'https://www.maodou.com/www/fyc/brifinfo/3kC', 'https://www.maodou.com/www/fyc/brifinfo/3gC', 'https://www.maodou.com/www/fyc/brifinfo/3fC', 'https://www.maodou.com/www/fyc/brifinfo/CXC', 'https://www.maodou.com/www/fyc/brifinfo/w7C', 'https://www.maodou.com/www/fyc/brifinfo/wOC', 'https://www.maodou.com/www/fyc/brifinfo/CVC', 'https://www.maodou.com/www/fyc/brifinfo/wWC', 'https://www.maodou.com/www/fyc/brifinfo/wkC', 'https://www.maodou.com/www/fyc/brifinfo/3ZC', 'https://www.maodou.com/www/fyc/brifinfo/CEC', 'https://www.maodou.com/www/fyc/brifinfo/C1C', 'https://www.maodou.com/www/fyc/brifinfo/3jC', 'https://www.maodou.com/www/fyc/brifinfo/3lC', 'https://www.maodou.com/www/fyc/brifinfo/wKC', 'https://www.maodou.com/www/fyc/brifinfo/wJC', 'https://www.maodou.com/www/fyc/brifinfo/woC', 'https://www.maodou.com/www/fyc/brifinfo/wyC', 'https://www.maodou.com/www/fyc/brifinfo/wMC', 'https://www.maodou.com/www/fyc/brifinfo/3EC', 'https://www.maodou.com/www/fyc/brifinfo/33C', 'https://www.maodou.com/www/fyc/brifinfo/C9C', 'https://www.maodou.com/www/fyc/brifinfo/3SC', 'https://www.maodou.com/www/fyc/brifinfo/yCC', 'https://www.maodou.com/www/fyc/brifinfo/y3C', 'https://www.maodou.com/www/fyc/brifinfo/wbC', 'https://www.maodou.com/www/fyc/brifinfo/wXC', 'https://www.maodou.com/www/fyc/brifinfo/w4C', 'https://www.maodou.com/www/fyc/brifinfo/C7C', 'https://www.maodou.com/www/fyc/brifinfo/wDC', 'https://www.maodou.com/www/fyc/brifinfo/CRC', 'https://www.maodou.com/www/fyc/brifinfo/C8C', 'https://www.maodou.com/www/fyc/brifinfo/wBC', 'https://www.maodou.com/www/fyc/brifinfo/wPC']
	# start_urls = ['https://www.maodou.com/www/fyc/brifinfo/CVC']

	def parse(self, response):
		driver = self.driver
		driver.get(response.url)
		item = items.GetMaodouItem()
		soup = BeautifulSoup(driver.page_source, 'xml')
		num = len(soup.find_all('div', {'class': 'banner-right'})[0].find_all('span'))
		print(num)
		if num < 4:
			item['name'] = soup.find_all('h2', {'class': 'banner-tit'})[0].get_text()
			item['factoryprice'] = soup.find_all('div', {'class': 'banner-right'})[0].find_all('p', {'class':'price '})[0].get_text()[6:]
			item['shoufu'] = soup.find_all('div', {'class': 'banner-right'})[0].find_all('p', {'class':'sy-num'})[0].get_text()
			item['yuegong'] = soup.find_all('div', {'class': 'banner-right'})[0].find_all('p', {'class':'yf-num sy-num'})[0].get_text()
		# if len(soup.find_all('div', {'class': 'banner-right'})[0].find_all('span'))>3:
		#     item['fenqi'] = str(soup.find_all('div', {'class': 'banner-right'})[0].find_all('span')[1].get_text()) + '*' + str(soup.find_all('div', {'class': 'banner-right'})[0].find_all('span')[2].get_text())
		#     item['quankuan'] = soup.find_all('div', {'class': 'banner-right'})[0].find_all('span')[3].get_text()
		# else:
			item['fenqi'] = str(soup.find_all('div', {'class': 'banner-right'})[0].find_all('span')[0].get_text()) + '*' + str(soup.find_all('div', {'class': 'banner-right'})[0].find_all('span')[1].get_text())
			item['quankuan'] = soup.find_all('div', {'class': 'banner-right'})[0].find_all('span')[2].get_text()
			item['qishu'] = soup.find_all('div', {'class': 'banner-right'})[0].find_all('p', {'class':'yf-num sy-num'})[1].get_text()
			yield item