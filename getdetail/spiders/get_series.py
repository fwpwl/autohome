# -*- coding: utf-8 -*-

import scrapy
from getdetail import items
from scrapy.http import Request
import json
import pymysql.cursors


brands = [204, 68, 147, 128, 191, 167, 190, 20, 146, 98, 47, 114, 100, 157, 88, 165, 4, 22, 202, 132, 175, 201, 134, 87, 15, 38, 63, 39, 79, 31, 172, 28, 123, 23, 159, 185, 104, 140, 142, 19, 127, 122, 8, 161, 162, 89, 108, 95, 198, 184, 106, 118, 117, 195, 152, 7, 115, 171, 119, 40, 138, 82, 30, 193, 77, 64, 97, 149, 126, 101, 9, 27, 206, 73, 55, 169, 60, 16, 86, 196, 10, 139, 76, 34, 3, 53, 36, 166, 168, 133, 144, 41, 72, 203, 50, 57, 84, 207, 37, 48, 74, 56, 120, 170, 141, 192, 66, 90, 116, 44, 42, 71, 17, 91, 125, 62, 59, 137, 65, 194, 67, 61, 35, 143, 54, 174, 26, 197, 99, 158, 45, 18, 131, 70, 199, 46, 12, 21, 14, 5, 81, 156, 13, 136, 1, 111, 113, 32, 164, 93, 209, 80, 176, 92, 52, 69, 85, 188, 29, 121, 102, 78, 96, 6, 109, 150, 105, 107, 11, 208, 145, 24, 163, 58, 148, 33, 112, 51, 153, 94, 2, 204, 68, 147, 128, 191, 167, 190, 20, 146, 98, 47, 114, 100, 157, 88, 165, 4, 22, 202, 132, 175, 201, 134, 87, 15, 38, 63, 39, 79, 31, 172, 28, 123, 23, 159, 185, 104, 140, 142, 19, 127, 122, 8, 161, 162, 89, 108, 95, 198, 184, 106, 118, 117, 195, 152, 7, 115, 171, 119, 40, 138, 82, 30, 193, 77, 64, 97, 149, 126, 101, 9, 27, 206, 73, 55, 169, 60, 16, 86, 196, 10, 139, 76, 34, 3, 53, 36, 166, 168, 133, 144, 41, 72, 203, 50, 57, 84, 207, 37, 48, 74, 56, 120, 170, 141, 192, 66, 90, 116, 44, 42, 71, 17, 91, 125, 62, 59, 137, 65, 194, 67, 61, 35, 143, 54, 174, 26, 197, 99, 158, 45, 18, 131, 70, 199, 46, 12, 21, 14, 5, 81, 156, 13, 136, 1, 111, 113, 32, 164, 93, 209, 80, 176, 92, 52, 69, 85, 188, 29, 121, 102, 78, 96, 6, 109, 150, 105, 107, 11, 208, 145, 24, 163, 58, 148, 33, 112, 51, 153, 94, 2]


class BrandsSpider(scrapy.Spider):
    name = "d_series"
    start_urls = []
    for i in brands:
        start_urls.append('https://m.zjurl.cn/motor/brand/m/v1/series/?brand_id=%s'%i)

    def parse(self, response):
        res = json.loads(response.body)
        info = res['data']
        for k in info:
            if 'series_name' in k['info']:
                item = items.GetSeriesItem()
                item['id'] = k['info']['series_id']
                item['name'] = k['info']['series_name']
                yield item