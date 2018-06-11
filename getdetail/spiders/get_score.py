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


config = {
          'host':'127.0.0.1',
          'port': 3306,
          'user':'root',
          'password':'123',
          'db':'scrapy',
          'charset':'utf8mb4',
          }
connection = pymysql.connect(**config)


class ScoreSpider(scrapy.Spider):
    name = "score"
    start_urls = []
    try:
        with connection.cursor() as cursor:
            sql = "select id from series"
            cursor.execute(sql)
            for id in cursor.fetchall():
                start_urls.append('https://www.autohome.com.cn/%s' % id[0])
    except Exception as e:
        print("update series fail %s" % e)

    def parse(self, response):
        item = items.ScoreItem()
        series_id = response.url.split('/')[-1]
        item['series_id'] = int(series_id)
        sc = response.xpath('//div[@class="koubei-score"]/div')
        if not sc:
            item['score'] = '暂无评分'
        else:
            score = sc[0].xpath('./a[@class="font-score"]/text()').extract()
            if not score:
                item['score'] = '暂无评分'
            else:
                item['score'] = score[0]
        yield item
    connection.close()