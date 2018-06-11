# -*- coding: utf-8 -*-

import scrapy
import string
from getdetail import items
import logging
from scrapy.http import Request
import json
import pymysql.cursors
from selenium import webdriver


config = {
          'host': '192.168.10.100',
          'port': 3306,
          'user': 'afsaas',
          'password': '218F2AE2-F275-430B-A20B-1FD9E0CAD419',
          'db': 'cyx',
          'charset': 'utf8mb4',
          }
connection = pymysql.connect(**config)

def get_city_id(city):
    with connection.cursor() as cursor:
        sql = "select id from areas where pid!=0 and name=%s"
        cursor.execute(sql, (city))
        id = cursor.fetcone()
        if id:
            return id['id']
        else:
            return 0

class BrandsSpider(scrapy.Spider):

    name = "cutprice"
    start_urls = []
    with connection.cursor() as cursor:
        sql = "select id from series where id not in(select distinct series_id from cut_price)"
        cursor.execute(sql)
        for id in cursor.fetchall():
            for i in range(1, 6):
                start_urls.append('https://buy.m.autohome.com.cn/PreVerSeries/GetSeriesSpecListAjax?provinceId=0&cityId=0&seriesId=%s&specId=0&pageSize=100&pageIndex=%s'%(id[0], i))

    def parse(self, response):
        try:
            res = json.loads(response.text)
        except:
            return
        if not res:
            return
        item = items.GetPriceItem()
        item['series_id'] = res['SeriesId']
        spec_list = res['SpecList']
        for spec in spec_list:
            item['car_id'] = spec['SpecID']
            item['ori_price'] = spec['OriginalPriceM']
            item['per_price'] = spec['PriceM']
            item['d_price'] = spec['PriceOffM']
            item['stock'] = spec['InventoryStateDesc']
            item['dealer_id'] = spec['DealerId']
            item['city'] = spec['CityName']
            item['city_id'] = 0
            # item['city_id'] = spec['CityId']

            yield item
    connection.close()
