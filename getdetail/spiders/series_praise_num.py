# -*- coding: utf-8 -*-

import scrapy
import string
from getdetail import items
import logging
from scrapy.http import Request
import json
import pymysql.cursors
import re
import random


config = {
          'host': '192.168.10.100',
          'port': 3306,
          'user': 'afsaas',
          'password': '218F2AE2-F275-430B-A20B-1FD9E0CAD419',
          'db': 'cyx',
          'charset': 'utf8mb4',
          }
connection = pymysql.connect(**config)


class ScoreSpider(scrapy.Spider):
    name = "praise_num"
    start_urls = []
    try:
        with connection.cursor() as cursor:
            sql = "select id from series where has_scene=1"
            cursor.execute(sql)
            ids = [526, 314, 4487, 448, 3582, 3204, 3554, 4490, 3824, 3462, 3852, 364, 4074, 4491, 3294, 3780, 623, 4139, 2886, 4370, 4226, 2863, 4376, 882, 3126, 2566, 407, 4242, 4115, 2768, 4259, 2319, 3618, 2333, 4069, 3413, 4151, 2852, 4472, 3426, 4130, 3693, 2791, 4387, 4505, 4523, 4394, 2228, 3043, 4092, 3430, 793, 3553, 3201, 3068, 3426, 4298, 3777, 95, 4200, 749, 750, 398, 3652, 373, 3081, 758, 3234, 4385, 3576, 3562, 4502, 178, 4043, 52, 3312, 2761, 4029, 3158, 4240, 4263, 2743, 56, 4291, 620, 1004, 4095, 209, 4174, 557, 2717, 2723, 4074, 3793, 3874, 2967, 2941, 4569]
            # for id in cursor.fetchall():
            for id in ids:
                start_urls.append('https://www.autohome.com.cn/%s' % id)
    except Exception as e:
        print("update series fail %s" % e)
    

    def parse(self, response):
        urls = []
        item = {}
        id = response.url.split('/')[-1]
        item['id'] = int(id)
        sc = response.xpath('//div[@class="autoseries-pic-img2 autoseries-pic-img-vr"]/a/@href').extract()
        if sc:
          urls.append(sc[0])
        for url in urls:
            yield Request(url, meta={'id': id}, callback=self.parse_scene)

    def parse_scene(self, response):
      item = items.PraiseNumItem()
      res = response.text
      start = res.find('var globalConfig')
      if start == -1:
        return
      start = res.find("{", start)
      if start == -1:
        return
      end = res.find('};', start)
      if end == -1:
        return
      res = res[start: end+1]
      s = res.find('like: "')
      if s == -1:
        return
      e = res.find('",', s)
      rv = res[s: e]
      num = rv[7:]
      item['praise_num'] = random.randint(1,int(int(num)*0.1))
      item['id'] = int(response.meta['id'])
      yield item

    