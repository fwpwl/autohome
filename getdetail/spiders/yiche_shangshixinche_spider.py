# -*- coding: utf-8 -*-
import scrapy
from getdetail import items
from scrapy.http import Request
import json
import pymysql.cursors


config = {
          'host': '192.168.10.100',
          'port': 3306,
          'user': 'afsaas',
          'password': '218F2AE2-F275-430B-A20B-1FD9E0CAD419',
          'db': 'cyx',
          'charset': 'utf8mb4',
          }
connection = pymysql.connect(**config)

def get_sid(name):
    with connection.cursor() as cursor:
        sql = "select id from series where name=%s"
        cursor.execute(sql, (name))
        id = cursor.fetchone()
        if id:
            return id[0]
        return 0

def get_ntype(tag):
    if tag == 1:
        return '全新车型'
    elif tag == 2:
        return '换代车型'
    elif tag == 3:
        return '改款车型'
    elif tag == 4:
        return '新增车款'
    else:
        return None

def get_time(year, month):
    if len(month) < 2:
        month = '0' + month
    return year + month

def get_maxprice(price):
    print(price)
    if '-' in price:
        return int(float(price.split('-')[1][:-1])*10000)
    else:
        return int(float(price[:-1])*10000)

def get_minprice(price):
    if '-' in price:
        return int(float(price.split('-')[0])*10000)
    else:
        return int(float(price[:-1])*10000)

class YiCheCarsSpider(scrapy.Spider):

    name = "yiche_cars"
    start_urls = [
        'https://carapi.app.yiche.com/car/GetSerialInfoForNewByMonth?year=2018&month=1&pageindex=1&pagesize=200',
        'https://carapi.app.yiche.com/car/GetSerialInfoForNewByMonth?year=2018&month=2&pageindex=1&pagesize=200',
        'https://carapi.app.yiche.com/car/GetSerialInfoForNewByMonth?year=2018&month=3&pageindex=1&pagesize=200',
        'https://carapi.app.yiche.com/car/GetSerialInfoForNewByMonth?year=2018&month=4&pageindex=1&pagesize=200',
        'https://carapi.app.yiche.com/car/GetSerialInfoForNewByMonth?year=2018&month=5&pageindex=1&pagesize=200',
        'https://carapi.app.yiche.com/car/GetSerialInfoForNewByMonth?year=2018&month=6&pageindex=1&pagesize=200',
        'https://carapi.app.yiche.com/car/GetSerialInfoForNewByMonth?year=2018&month=7&pageindex=1&pagesize=200',
        ]

    def parse(self, response):
        res = json.loads(response.text)
        cars_list = res['data']
        for k in cars_list:
            item = items.GetNewCarsItem()
            item['name'] = k['CsName']
            item['img_url'] = k['CoverImage']
            item['series_id'] = get_sid(item['name'])
            item['sale_at'] = get_time(str(k['MYear']), str(k['MMonth']))
            item['ntype'] = get_ntype(int(k['CarTag']))
            item['level'] = k['Level']
            item['price'] = k['RefPrice']
            yield item
