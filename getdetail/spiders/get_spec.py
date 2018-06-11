# -*- coding: utf-8 -*-

import scrapy
import string
from getdetail import items
import re
import json
import logging
from scrapy.http import Request
import json
import pymysql.cursors
import logging


config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'123',
          'db':'scrapy',
          'charset':'utf8mb4',
          }
connection = pymysql.connect(**config)

def get_car_id(id):
    try:
        with connection.cursor() as cursor:
            sql = "select id from specs where id=%s"
            cursor.execute(sql, (id))
            id = cursor.fetchone()
            if id:
                return id['id']
            else:
                return None
    except Exception as e:
        return None

def get_column_id(name):
    try:
        with connection.cursor() as cursor:
            sql = "select id from columns where name=%s"
            cursor.execute(sql, (name))
            id = cursor.fetchone()
            if id:
                return id
    except Exception as e:
        return None


class SpecsSpider(scrapy.Spider):
    name = "spec"
    all_series = []
    start_urls = []
    for letter in string.ascii_uppercase:
      url ='https://car.autohome.com.cn/config/series/3811.html'
      start_urls.append(url)


    # def parse(self, response):
    #     series_a_list = None
    #     brands = response.xpath('//dl')
    #     # for dl in brands:
    #         # dt = dl.css('dt>a::attr(href)').extract_first()
    #         # brand_id = re.search(r"brand-(\d+).html", dt).group(1)
    #         # try:
    #         #     series_a_list = dl.xpath('.//dd//li//h4//a').extract()
    #         # except Exception as e:
    #         #     series_a_list = None
    #         # if series_a_list:
    #         #     items = []
    #         #     for a in series_a_list:
    #         #         tmp = re.search(r"autohome.com.cn/(\d+)/#.*>(.+)</a>", a)
    #         #         sid = tmp.group(1)
    #         #         items.append(sid)
    #     sid = 3811
    #         # 请求所有车型的
    #         # for sid in items:
    #     yield Request('https://car.autohome.com.cn/config/series/3811.html', meta={'series_id': sid}, callback=self.parse_series_get_car_id)

    def parse(self, response):
        series_id = 3811
        ids = []
        # try:
        #   ids = re.search("var specIDs =\[(.+?)\];", str(response.body)).group(1)
        #   print(ids)
        # except Exception as e:
        #   logging.debug('NO ids %s', e)
        #   return
        # if ids:
        #     ids = [int(x) for x in ids.split(',')]
        # if not ids:
        #     print('='*20)
        #     print('没有匹配到car_ids')
        #     print('='*20)
        # else:
        ids = [33097, 32966, 33098,33099,33100,33022,30781]
        for id in ids:
            yield Request('https://car.m.autohome.com.cn/ashx/car/GetModelConfig.ashx?ids=%s'% id, meta={'car_id': id, 'series_id': series_id}, callback=self.parse_spec)

    def parse_spec(self, response):
        """ 分析匹配车型网页获取配置信息
        """
        res = json.loads(response.body.decode('utf-8'))
        item = items.SpecItem()
        config = res['config'] + res['param']
        items_list = []
        for c in config:
            if "paramitems" in c:
                items_list.append(c['paramitems'])
            elif 'configitems' in c:
                items_list.append(c['configitems'])
        col = {}
        for it in items_list:
            for c in it:
                col[c['name']] = c['valueitems'][0]['value']

        columns_dict = {}
        for k, v in col.items():
            id = get_column_id(k)
            if id:
                columns_dict['i' + str(id[0])] = v
        item['id'] = int(response.meta['car_id'])
        car_id = get_car_id(item['id'])
        if not car_id:
          item['series_id'] = int(response.meta['series_id'])
          item['i1'] = columns_dict['i1']
          item['i2'] = columns_dict['i2']
          item['i3'] = columns_dict['i3']
          item['i4'] = columns_dict['i4']
          item['i5'] = columns_dict['i5']
          item['i6'] = columns_dict['i6']
          item['i7'] = columns_dict['i7']
          item['i8'] = columns_dict['i8']
          item['i9'] = columns_dict['i9']
          item['i10'] = columns_dict['i10']
          item['i11'] = columns_dict['i11']
          item['i12'] = columns_dict['i12']
          item['i13'] = columns_dict['i13']
          item['i14'] = columns_dict['i14']
          item['i15'] = columns_dict['i15']
          item['i16'] = columns_dict['i16']
          item['i17'] = columns_dict['i17']
          item['i18'] = columns_dict['i18']
          item['i19'] = columns_dict['i19']
          item['i20'] = columns_dict['i20']
          item['config'] = json.dumps(columns_dict)
          yield item
