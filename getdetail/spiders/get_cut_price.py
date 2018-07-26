# - coding: utf-8 -*-
import scrapy
import string
from getdetail import items
import logging
from scrapy.http import Request
import json
import pymysql.cursors
import re


config = {
        'host':'127.0.0.1',
        'port':3306,
        'user':'root',
        'password':'123',
        'db':'cyx',
        'charset':'utf8mb4',
        }
connection = pymysql.connect(**config)

def cut_price(car_id,dealer_id):
        try:
            with connection.cursor() as cursor:
                sql = "select car_id from cut_price where dealer_id =%s and car_id =%s"
                cursor.execute(sql, (car_id,dealer_id))
                id = cursor.fetchone()
                if id:
                    return True
                else:
                    return None
        except Exception as e:
            return None           

class Get_CutPriceSpider(scrapy.Spider):
    name = "get_cutprice"
    start_urls = []

    try:
        with connection.cursor() as cursor:
            sql = "select id from series"
            cursor.execute(sql)
            for id in cursor.fetchall():
                for i in range(1,5):
                    start_urls.append('https://buy.m.autohome.com.cn/handler/buy/GetBuyPriceList?cityId=0&seriesId=%s&specId=0&pageIndex=%s&pageSize=10&orderBy=5&distance=200&rcmLessThanNum=3'%(str(id[0]),i))
    except Exception as e:
        print("update series fail %s" % e)

    def parse(self, response):
        try:
            res = json.loads(response.text)
        except:
            return
        if not res:
            return
        item = items.EcarsssItem()
        for i in res:
            car_id = i['SpecId']
            series_id = i['SeriesId']
            ori_price = i['OriginalPrice']
            per_price = i['Price']
            d_price = i['PriceOff']
            city = i['CityName']
            city_id = i['CityId']
            dealer_id = i['DealerId']

            rv = cut_price(dealer_id,car_id)
            if rv:
               return
            else:
                series_id = i['SeriesId']
                item['dealer_id'] = i['DealerId']
                item['car_id'] = i['SpecId']
                item['series_id'] = i['SeriesId']
                item['ori_price'] = i['OriginalPrice']
                item['per_price'] = i['Price']
                item['dealer_id'] = i['DealerId']
                item['d_price'] = i['PriceOff']
                item['city'] = i['CityName']
                item['stock'] = ''
                item['city_id'] = i['CityId']
                yield item