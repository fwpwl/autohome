# -*- coding: utf-8 -*-

import scrapy
import string
from getdetail import items
import logging
from scrapy.http import Request
import json
import pymysql.cursors
from selenium import webdriver


# config = {
#           'host': '192.168.9.100',
#           'port': 3306,
#           'user': 'afsaas',
#           'password': '218F2AE2-F275-430B-A20B-1FD9E0CAD419',
#           'db': 'afsaas',
#           'charset': 'utf8mb4',
#           }
# connection = pymysql.connect(**config)

class DealersSpider(scrapy.Spider):
    name = "dealers"
    start_urls = []
    for i in range(1, 31):
      start_urls.append('https://buy.m.autohome.com.cn/PreVerSeries/GetSeriesSpecListAjax?provinceId=0&cityId=0&seriesId=59&specId=0&pageSize=10&pageIndex=%s'%i)

    def parse(self, response):
        res = json.loads(response.text)
        item = items.DealersItem()
        spec_list = res['SpecList']
        for spec in spec_list:
            item['id'] = spec['DealerId']
            item['name'] = spec['CompanySimple']
            item['address'] = spec['Address']
            item['sell_phone'] = spec['SellPhone']
            item['sale_range'] = spec['OrderRangeName']
            item['sale_to'] = spec['OrderRangeTitle']
            item['city'] = spec['CityName']
            yield item
    # connection.close()