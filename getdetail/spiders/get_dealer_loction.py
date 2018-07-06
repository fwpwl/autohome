# -*- coding: utf-8 -*-

import scrapy
from getdetail import items
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

def get_loc(lon, lat):
    loc = 'point(%s %s)'%(lon, lat)
    return loc


class DealersSpider(scrapy.Spider):
    name = "dealer_loction"
    start_urls = []
    try:
        with connection.cursor() as cursor:
            sql = "select id from dealers"
            cursor.execute(sql)
            for id in cursor.fetchall():
                start_urls.append('https://dealer.autohome.com.cn/Ajax/GetDealerInfo?DealerId=%s'%id[0])
    except Exception as e:
        print("add url fail %s" % e)


    def parse(self, response):
        res = json.loads(response.text)
        item = items.DealerLoctionItem()
        item['id'] = res['DealerId']
        item['province_id'] = res['PID']
        item['city_id'] = res['CID']
        item['sid'] = res['SID']
        item['loc'] = get_loc(res['MapLonBaidu'], res['MapLatBaidu'])
        item['lon'] = res.get('MapLonBaidu', 0)
        item['lat'] = res.get('MapLatBaidu', 0)
        yield item
