# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from lxml import etree
from brands.items import BrandsItem
from xpinyin import Pinyin
import pymysql.cursors



class BrandsspiderSpider(scrapy.Spider):
    name = 'brandsspider'
    allowed_domains = ['autohome.com']
    start_urls = ['https://car.m.autohome.com.cn/']


    def parse(self, response):
        driver = webdriver.Chrome()
        driver.get(response.url)
        source = driver.page_source
        dom = etree.HTML(source)
        items = dom.xpath("//div[@id='div_ListBrand']/div/text()")
        s_id = []
        P = Pinyin()

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
                sql = "select * from brands"
                cursor.execute(sql)

                for i in cursor.fetchall():
                    _id = i['id']
                    s_id.append(_id)
        except Exception as e:
            print(e)


        lists = dom.xpath("//div[@id='div_ListBrand']/ul")
        for l,i in zip(lists,items):

            names = l.xpath("./li/div/span/text()")
            ids = l.xpath("./li/@v")
            logos = l.xpath(".//img/@src|.//img/@data-src")

            for name, id, logo in zip(names, ids, logos):
                if int(id) not in s_id:
                    item = BrandsItem()
                    item['items'] = i
                    item['name'] = name

                    item['id'] = id
                    item['logo'] = 'http://cdn.autoforce.net/cyx/images/brands/' + id + '.' + logo.split('.')[-1]
                    item['status'] = 0
                    item['images'] = response.urljoin(logo)
                    item['spell'] = P.get_pinyin(u"%s" % name, '')
                    yield item





