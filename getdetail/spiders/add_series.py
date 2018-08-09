# -*- coding: utf-8 -*-
import scrapy
import pymysql
import pymysql.cursors
import json
from getdetail.items import SeriesItem
def get_id_mysql():
    #根据name从数据brands表来获得id
    names = ['现代','宝马','中华','五菱汽车','领克','众泰','三菱',]

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
            sql = "select * from brands"
            cursor.execute(sql)
            id = []
            for a in cursor.fetchall():
                if a['name'] in names:
                    id.append(a['id'])
            return id

    except Exception as e:
        print(e)
    finally:

        BBB.close()






class SeriesspiderSpider(scrapy.Spider):
    name = 'add_series'

    def start_requests(self):
        reqs = []
        #获得该车系的品牌ｉｄ
        # brands =[1]
        brands = get_id_mysql()
        for i in brands:
            req = scrapy.Request('https://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?r=6s&b=%s' %i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        brand_id = response.url.split('b=')[1]

        names = ['宝马X2','中华V7','宝骏360','ENCINO 昂希诺','领克02','众泰T800','奕歌']
        data = json.loads(response.text)['result']['sellSeries']
        for f in data:
            factory = f['name']
            text = f['SeriesItems']
            for x in text:

                item = SeriesItem()
                #通过车系的名称来寻找车系数据
                if x['name'] in names:
                    item['id'] = x['id']
                    item['maxprice'] = x['maxprice']
                    item['minprice'] = x['minprice']
                    item['name'] = x['name']
                    item['factory'] = factory
                    item['brand_id'] = brand_id
                    item['img_url'] = 'http://cdn.autoforce.net/cyx/images/series/%s.png' % x['id']
                    item['d_url'] = 'http://cdn.autoforce.net/cyx/images/d_series/%s.jpg' % x['id']
                    s_url = 'https://m.autohome.com.cn/%s' % x['id']
                    yield scrapy.Request(url=s_url, meta={'item': item}, callback=self.parse_item, dont_filter=True)


    def parse_item(self, response):

        item = response.meta['item']
        aaa = response.xpath("//div[@class='deploy']/span[2]/text()").extract()[0][4:]
        if aaa != '暂无':
            item['grade'] = response.xpath("//div[@class='deploy']/span[1]/text()").extract()[1][2:]+' '+aaa
        else:
            item['grade'] = response.xpath("//div[@class='deploy']/span[1]/text()").extract()[1][2:]

        print(item['grade'])
        yield item










