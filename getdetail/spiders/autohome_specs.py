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
          'host': '192.168.10.100',
          'port': 3306,
          'user': 'afsaas',
          'password': '218F2AE2-F275-430B-A20B-1FD9E0CAD419',
          'db': 'cyx',
          'charset': 'utf8mb4',
		}
connection = pymysql.connect(**config)

def get_car_id(id):
	try:
		with connection.cursor() as cursor:
			sql = "select id from specs where id=%s"
			cursor.execute(sql, (id))
			id = cursor.fetchone()
			if id:
				print('result', id)
				return id[0]
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
		name = "autohome_specs"
		start_urls = ['https://car.m.autohome.com.cn/']

		def parse(self, response):
			brands_ids = re.findall(r'id="sp_(\d+?)"', response.text)
			for b in brands_ids:
				yield Request('https://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?r=6s&b=%s'%int(b), meta={'brand_id': int(b)}, callback=self.parse_series)

		def parse_series(self, response):
			brand_id = response.meta['brand_id']
			res = json.loads(response.text)
			if not res['result']['sellSeries']:
				return
			else:
				series_list = res['result']['sellSeries'][0]['SeriesItems']
				for s in series_list:
					series_id = s['id']
					yield Request('https://m.autohome.com.cn/car/series/ashx/GetSpecPriceListBySeriesId.ashx?seriesId=%s'% series_id, meta={'series_id': series_id}, callback=self.parse_car_id)

		def parse_car_id(self, response):
			series_id = response.meta['series_id']
			res = json.loads(response.text)
			if not res:
				return
			for k in res:
				id = k['specid']
				yield Request('https://car.m.autohome.com.cn/ashx/car/GetModelConfig.ashx?ids=%s'% id, meta={'car_id': id, 'series_id': series_id}, callback=self.parse_spec)

		def parse_spec(self, response):
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
			print(item['id'])
			car_id = get_car_id(item['id'])
			print(car_id)
			if not car_id:
				item['series_id'] = int(response.meta['series_id'])
				item['i1'] = columns_dict['i1']
				item['i2'] = columns_dict['i2']
				item['i3'] = columns_dict['i3']
				item['i4'] = columns_dict['i4']
				item['i5'] = columns_dict['i5']
				item['i6'] = columns_dict.get('i6', '')
				item['i7'] = columns_dict.get('i7', '')
				item['i8'] = columns_dict.get('i8', '')
				item['i9'] = columns_dict.get('i9', '')
				item['i10'] = columns_dict.get('i10', '')
				item['i11'] = columns_dict.get('i11', '')
				item['i12'] = columns_dict.get('i12', '')
				item['i13'] = columns_dict.get('i13', '')
				item['i14'] = columns_dict.get('i14', '')
				item['i15'] = columns_dict.get('i15', '')
				item['i16'] = columns_dict.get('i16', '')
				item['i17'] = columns_dict.get('i17', '')
				item['i18'] = columns_dict.get('i18', '')
				item['i19'] = columns_dict.get('i19', '')
				item['i20'] = columns_dict.get('i20', '')
				columns_dict = re.sub(r'&nbsp;', '', str(columns_dict))
				item['config'] = json.dumps(eval(columns_dict))
				columns_dict = eval(columns_dict)

				i300 = item['i2']
				if len(i300) > 10:
					i300 = i300.split('~')[0]
				try:
					item['i300'] = float(i300[:-1])
				except Exception as e:
					item['i300'] = 0

				
				i301 = columns_dict.get('i35', '')
				try:
					if i301.isdigit():
						item['i301'] = int(i301)
					else:
						item['i301'] = 0
				except Exception as e:
					item['i301'] = 0

				i302 = columns_dict.get('i30', '')
				i30 = ''
				try:
					if 0 < len(i302) < 3:
						i30 = i302
					elif len(i302) >= 3:
						arr1 = i302.split('/')
						if len(arr1) > 1:
							str_tmp = ''
							for i in arr1:
								if int(i) < 8:
									str_tmp += i
									str_tmp += ','
								elif int(i) > 7:
									str_tmp += '10'
									break
							i30 = str_tmp
						else:
							arr2 = i302.split('-')
							str_tmp = ''
							if len(arr2) > 1:
								begin = int(arr2[0])
								end = int(arr2[1])
								for i in range(begin, end+1):
									if i < 8:
										str_tmp += str(i)
										str_tmp += ','
									elif i > 7:
										str_tmp += '10'
										break
								i30 = str_tmp

				except Exception as e:
					item['i302'] = 0
				item['i302'] = i30

				i303 = columns_dict.get('i57', '')
				if '手动' in i303:
					item['i303'] = 1
				else:
					item['i303'] = 2

				i304 = columns_dict.get('i36', '')
				if '自然吸气' in i304:
					item['i304'] = 1
				elif '涡轮增压' in i304:
					item['i304'] = 2
				elif '机械增压' in i304:
					item['i304'] = 3
				else:
					item['i304'] = 0

				i305 = columns_dict.get('i59', '')
				if '前驱' in i305:
					item['i305'] = 1
				elif '前驱' in i305:
					item['i305'] = 2
				elif '前驱' in i305:
					item['i305'] = 3
				else:
					item['i305'] = 0

				i306 = columns_dict.get('i108', '-')
				if i306 == '-':
					item['i306'] = 0
				else:
					item['i306'] = 1

				i307 = columns_dict.get('i107', '-')
				if i307 == '-':
					item['i307'] = 0
				else:
					item['i307'] = 1

				i308 = columns_dict.get('i145', '-')
				if i308 == '-':
					item['i308'] = 0
				else:
					item['i308'] = 1

				i309 = columns_dict.get('i82', '-')
				if i309 == '-':
					item['i309'] = 0
				else:
					item['i309'] = 1

				i310 = columns_dict.get('i170', '-')
				if '氙气' not in i310:
					item['i310'] = 0
				else:
					item['i310'] = 1

				i311 = columns_dict.get('i155', '-')
				if i311 == '-':
					item['i311'] = 0
				else:
					item['i311'] = 1

				i312 = columns_dict.get('i91', '-')
				if i312 == '-':
					item['i312'] = 0
				else:
					item['i312'] = 1

				i313 = columns_dict.get('i135', '-')
				if '真皮' not in i313:
					item['i313'] = 0
				else:
					item['i313'] = 1

				i314 = columns_dict.get('i200', '-')
				if i314 == '-':
					item['i314'] = 0
				else:
					item['i314'] = 1

				i315 = columns_dict.get('i89', '-')
				if i315 == '-':
					item['i315'] = 0
				else:
					item['i315'] = 1

				i316 = columns_dict.get('i119', '-')
				if i316 == '-':
					item['i316'] = 0
				else:
					item['i316'] = 1

				i317 = columns_dict.get('i146', '-')
				if i317 == '-':
					item['i317'] = 0
				else:
					item['i317'] = 1

				i318 = columns_dict.get('i93', '-')
				if i318 == '-':
					item['i318'] = 0
				else:
					item['i318'] = 1

				grade1 = item['i4']
				if grade1 == '微型车':
					i319 = 1
				elif grade1 == '小型车':
					i319 = 2
				elif grade1 == '紧凑型车':
					i319 = 3
				elif grade1 == '中型车':
					i319 = 4
				elif grade1 == '中大型车':
					i319 = 5
				elif grade1 == '大型车':
					i319 = 6
				elif grade1 == '跑车':
					i319 = 7
				elif grade1 == 'MPV':
					i319 = 8
				elif 'SUV' in grade1:
					i319 = 9
				elif grade1 == '微面':
					i319 = 10
				elif grade1 == '微卡':
					i319 = 11
				elif grade1 == '轻客':
					i319 = 12
				elif grade1 == '皮卡':
					i319 = 13
				else:
					i319 = 0
				item['i319'] = i319

				grade2 = item['i12']
				print(grade2)
				if grade2 == '两厢车':
					i320 = 1
				elif grade2 == '三厢车':
					i320 = 2
				elif grade2 == '掀背车':
					i320 = 3
				elif grade2 == '旅行车':
					i320 = 4
				elif grade2 == '硬顶敞篷车':
					i320 = 5
				elif grade2 == '软顶敞篷车':
					i320 = 6
				elif grade2 == '硬顶跑车':
					i320 = 7
				elif grade2 == '客车':
					i320 = 8
				elif grade2 == '货车':
					i320 = 9
				else:
					i320 = 0
				item['i320'] = i320

				price = item['i2']
				print(price)
				if len(price) > 10:
					price = price.split('~')[0]
				price = price[:-1]
				if float(price) <= 10:
					i321 = 1
				elif 10<float(price)<=15:
					i321 = 2
				elif 15<float(price)<=25:
					i321 = 3
				elif float(price) >=30:
					i321 = 4
				else:
					i321 = 0
				item['i321'] = i321

				grade = item['i4']
				if grade == '微型车':
					i322 = 1
				elif grade == '小型车':
					i322 = 2
				elif grade == '紧凑型车':
					i322 = 3
				elif grade == '中型车':
					i322 = 4
				elif grade == '中大型车':
					i322 = 5
				elif grade == '大型车':
					i322 = 6
				elif grade == '跑车':
					i322 = 7
				elif grade == 'MPV':
					i322 = 8
				elif grade == '中型SUV':
					i322 = 9
				elif grade == '微面':
					i322 = 10
				elif grade == '微卡':
					i322 = 11
				elif grade == '轻客':
					i322 = 12
				elif grade == '皮卡':
					i322 = 13
				elif grade == '紧凑型SUV':
					i322 = 14
				elif grade == '中大型SUV':
					i322 = 15
				elif grade == '大型SUV':
					i322 = 16
				elif grade == '小型SUV':
					i322 = 17
				item['i322'] = i322

				yield item
