# -*- coding: utf-8 -*-

import scrapy
import string
from getdetail import items
import logging
from scrapy.http import Request
import json
import pymysql.cursors
from selenium import webdriver
import re


config = {
          'host': '127.0.0.1',
          'port': 3306,
          'user': 'root',
          'password': '123',
          'db': 'cyx',
          'charset': 'utf8mb4',
          }
connection = pymysql.connect(**config)

class DealersSpider(scrapy.Spider):
    name = "dealer_series"
    start_urls = []
    try:
        with connection.cursor() as cursor:
            sql = "select id from series"
            cursor.execute(sql)
            for id in cursor.fetchall():
                start_urls.append('https://dealer.m.autohome.com.cn/api/BaseData/GetDealerListPager?seriesId=%s&specId=0&kindId=1&pageIndex=1&cityId=0&pageSize=100&orderType=0&type=1&lat=&lon='%id[0])
    except Exception as e:
        print("update series fail %s" % e)

    def parse(self, response):
        urls = []
        res = json.loads(response.text)
        nums = res['result']['pagecount']
        series_id = int(re.findall(r'seriesId=(\d+)\&specId', response.url)[0])
        if nums < 1:
            return
        else:
            for i in range(1, nums+1):
                urls.append('https://dealer.m.autohome.com.cn/api/BaseData/GetDealerListPager?seriesId=%s&specId=0&kindId=1&pageIndex=%s&cityId=0&pageSize=100&orderType=0&type=1&lat=&lon='%(series_id, i))
        for url in urls:
            yield Request(url, callback=self.parse_spec)

        
    def parse_spec(self, response):
        res = json.loads(response.text)
        item = items.DealerItem()
        spec_list = res['result']['list']
        for spec in spec_list:
            item['id'] = spec['DealerId']
            item['name'] = spec['CompanySimple']
            item['company'] = spec['Company']
            item['address'] = spec['Address']
            item['province_id'] = spec['ProvinceId']
            item['city_id'] = spec['CityId']
            item['county_id'] = spec['CountyId']
            item['saleto'] = spec['OrderRangeTitle']
            item['lon'] = spec['MapLonBaidu']
            item['lat'] = spec['MapLatBaidu']
            item['contacts'] = spec['LinkMan']
            item['city'] = spec['CityName']
            item['sale_range'] = spec['OrderRangeTitle']
            item['sellphone'] = spec['SellPhone']
            yield item

    connection.close()
