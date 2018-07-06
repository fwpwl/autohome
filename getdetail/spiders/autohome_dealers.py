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

def get_dealer_id(company, id):
    with connection.cursor() as cursor:
        sql = "select id from dealers where company=%s or id=%s"
        cursor.execute(sql, (company, id))
        id = cursor.fetchone()
        if id:
            return True
        return False

class DealersSpider(scrapy.Spider):
    name = "autohome_dealers"
    start_urls = []
    pages = 1675
    for i in range(1, pages+1):
        start_urls.append('https://dealer.autohome.com.cn/china/0/0/0/0/%s/1/0/0.html'%i)    
   
    def parse(self, response):
        res = response.xpath('//ul[@class="list-box"]/li/a/@href').extract()
        for k in res:
            id = k.split('/')[-2]
            url = 'https://dealer.autohome.com.cn/Ajax/GetDealerInfo?DealerId=%s'%id
            yield Request(url, callback=self.parse_spec)

    def parse_spec(self, response):
        spec = json.loads(response.text)
        item = items.DealersItem()
        item['id'] = spec['DealerId']
        item['company'] = spec['Company']
        rv = get_dealer_id(item['company'], item['id'])
        if rv:
            return
        else:
            item['name'] = spec['CompanySimple']
            item['address'] = spec['Address']
            item['province_id'] = spec['PID']
            item['city_id'] = spec['CID']
            item['county_id'] = spec['SID']
            item['sale_to'] = None
            item['contacts'] = None
            item['sale_range'] = spec['BusinessArea']
            item['sell_phone'] = spec['SellPhone']
            print(item)
            yield item
