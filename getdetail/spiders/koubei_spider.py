# -*- coding: utf-8 -*-

import scrapy
import json
from koubei.items import KoubeiItem
import re
import pymysql
import pymysql.cursors



def get_series_id(name):
    abc = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123',
        'db': 'cyx',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    bbb = pymysql.connect(**abc)
    try:
        with bbb.cursor() as cursor:
            sql = "select id from series where name = '%s'"%name
            cursor.execute(sql)
            for i in  cursor.fetchall():
                id = i['id']
                return id
            else:
                return None
    except Exception as e:
        print(e)
    finally:
        bbb.close()

def get_series_pub_():
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123',
            'db': 'cyx',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
        }
        connection = pymysql.connect(**config)

        try:
            with connection.cursor() as cursor:
                sql = 'select * from series_public_praise'
                cursor.execute(sql)
                dic = {}
                for i in cursor.fetchall():
                    id = i['id']
                    carname = i['carname']
                    reviewer = i['reviewer']
                    aaa = carname + ',' + reviewer
                    dic[aaa] = id
                return dic
        except Exception as e:
            print(e)
        finally:
            connection.close()


class KoubeiSpiderSpider(scrapy.Spider):

    name = 'koubei'

    def start_requests(self):
        reqs = []
        for i in range(1565, 10000):
            req = scrapy.Request(
                'http://carapi.ycapp.yiche.com/koubei/GetTopicListByServiceId?serviceId=%s&minid=0&pageSize=50&app_ver=8.9.2' % i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        if json.loads(response.text)['status']== 1:
            data = json.loads(response.text)['data']['result']
            if len(data)!=0:
                for i in data:
                    if len(i['topicInfo']['serialName'])!=0:
                        item = KoubeiItem()
                        key = i['topicInfo']['unionKey']
                        url = 'http://koubei.m.yiche.com/koubeidetail.html?g=%s'%key
                        item['series_name'] = i['topicInfo']['serialName']
                        item['series_id'] = get_series_id(item['series_name'])
                        item['carname'] = i['topicInfo']['trimName']
                        item['buy_city'] = i['topicInfo']['cityName']
                        item['title'] = ''
                        item['comment'] = i['topicInfo']['content']
                        item['publish_at'] = i['topicInfo']['createTime']
                        item['sat'] =i['topicInfo']['goodContent']
                        item['dissat'] = i['topicInfo']['badContent']
                        item['score'] = i['topicInfo']['rating']


                        yield scrapy.Request(url=url,meta={'item': item},callback=self.parse_item,dont_filter=True)

    def parse_item(self, response):
        item = response.meta['item']
        text = response.xpath("//div[@class='mess-box']/ul/li/text()").extract()
        for t in text:
            road = r'公里'
            pri = r'万'
            oil = r'km'
            buy = r'购于'
            roads = re.findall(road,t)
            pris = re.findall(pri,t)
            oils = re.findall(oil,t)
            buys = re.findall(buy,t)
            if len(pris)!=0:
                item['price'] = t
            if len(roads)!=0:
                item['road_haul'] =t
            if len(oils)!= 0:
                item['oil_wear'] = t
            if len(buys)!= 0:
                item['buy_at'] = t[3:]
        item['reviewer'] = response.xpath("//div[@class='user']/text()").extract()[2].strip()
        bbb = item['carname'] + ',' + item['reviewer']
        aa = get_series_pub_()
        key = list(aa.keys())
        if bbb in key:
            return

        if len(item['buy_city'])!=0 and len(item['price'])!=0 and len(item['oil_wear'])!=0 and len(item['comment'])!=0:
            yield item




