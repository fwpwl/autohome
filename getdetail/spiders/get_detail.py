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
import os
import sys


config = {
          'host':'127.0.0.1',
          'port': 3306,
          'user':'root',
          'password':'123',
          'db':'cyx',
          'charset':'utf8mb4',
          }
connection = pymysql.connect(**config)


class BrandsSpider(scrapy.Spider):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
    name = "series"
    start_urls = []
    try:
        with connection.cursor() as cursor:
            sql = "select id from series"
            cursor.execute(sql)
            for id in cursor.fetchall():
                start_urls.append('https://m.autohome.com.cn/%s' % id[0])
    except Exception as e:
        print("update series fail %s" % e)

    def parse(self, response):
        item = items.GetdetailItem()
        res = response.xpath('//section[@class="summary-series"]')
        p_div = res[0].xpath('.//div[@class="price"]/strong/text()').extract()[0]
        item['id'] = int(response.url.split('/')[-1])
        item['d_url'] = res[0].xpath('.//div[@class="thumb"]//a//img//@src').extract()[0]
        p = p_div.split('-')
        if len(p) > 1:
            item['minprice'] = int(float(p[0])*10000)
            item['maxprice'] = int(float(p[1])*10000)
            s = 'update cyx.series set maxprice=%s where id=%s'%(item['maxprice'], item['id']) + ';'
            print(s)
            logging.info(s)
        # else:
        #     item['minprice'] = 0
        #     item['maxprice'] = 0
        # grade = res[0].xpath('.//span/text()').extract()[1]
        # gra = comment = re.sub('\xa0', ' ', grade)
        # item['grade'] = gra
        
