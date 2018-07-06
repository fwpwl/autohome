# -*- coding: utf-8 -*-

import scrapy
import string
from getdetail import items
import logging
from scrapy.http import Request
import json
import pymysql.cursors


class ColumnsSpider(scrapy.Spider):
    name = "columns"
    start_urls = []
    start_urls.append('https://car.m.autohome.com.cn/ashx/car/GetModelConfig.ashx?ids=31058')

    def parse(self, response):
        res = json.loads(response.text)
        # config_list = res['param']
        config_list = res['config']
        for k in config_list:
            item = items.ColumnsItem()
            item['items'] = k['name']
            # for col in k['paramitems']:
            for col in k['configitems']:
                item['name'] = col['name']
                yield item
