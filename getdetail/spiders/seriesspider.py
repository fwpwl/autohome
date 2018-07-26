# -*- coding: utf-8 -*-
import scrapy
import pymysql
import pymysql.cursors
import json
from series.items import SeriesItem



def get_id(table_name,table_id):
    BBB = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123',
        'db': 'cyx',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    BBB = pymysql.connect(**BBB)
    try:
        with BBB.cursor() as cursor:
            sql = "select * from %s"%table_name
            cursor.execute(sql)
            for a in cursor.fetchall():
                table_id.append(a['id'])
            return table_id
    except Exception as e:
        print(e)
    finally:
        BBB.close()


class SeriesspiderSpider(scrapy.Spider):
    name = 'seriesspider'

    def start_requests(self):
        brands_id = []
        brands_id =  get_id('brands',brands_id)
        brands_id = get_id('brands1',brands_id)#通过俩次调用数据库函数，来获取所有的 brands  ID
        print(brands_id)
        reqs = []
        for i in brands_id:
            req = scrapy.Request('https://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?r=6s&b=%s' % int(i))
            reqs.append(req)
        return reqs

    def parse(self, response):

        brand_id = response.url.split('b=')[1]


        data = json.loads(response.text)['result']['sellSeries']
        for f in data:
            factory = f['name']
            text = f['SeriesItems']
            for x in text:
                item = SeriesItem()
                series_id = []
                series_id = get_id('series',series_id)#通过俩次调用数据库函数，来获取所有的 series  ID
                if x['id'] not in series_id:
                    item['id'] = x['id']
                    item['maxprice'] = x['maxprice']
                    item['minprice'] = x['minprice']
                    item['name'] = x['name']
                    item['factory'] = factory
                    item['brand_id'] = brand_id
                    item['img_url'] = 'http://cdn.autoforce.net/cyx/images/series/%s.png'%x['id']
                    item['d_url'] = 'http://cdn.autoforce.net/cyx/images/d_series/%s.jpg'%x['id']
                    s_url = 'https://m.autohome.com.cn/%s'%x['id']
                    yield  scrapy.Request(url=s_url,meta={'item': item},callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):

        item = response.meta['item']
        aaa = response.xpath("//div[@class='deploy']/span[2]/text()").extract()
        if aaa:
            aaa = aaa[0][4:]
            if aaa != '暂无':
                item['grade'] = response.xpath("//div[@class='deploy']/span[1]/text()").extract()[1][2:]+' '+aaa
            else:
                item['grade'] = response.xpath("//div[@class='deploy']/span[1]/text()").extract()[1][2:]
        else:
            item['grade'] = ''

        yield item










