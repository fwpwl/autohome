# -*- coding: utf-8 -*-

import scrapy
from getdetail import items
import json
import re
import pymysql.cursors

config = {
          'host': '127.0.0.1',
          'port': 3306,
          'user': 'root',
          'password': '123',
          'db': 'cyx',
          'charset': 'utf8mb4',
          }
connection = pymysql.connect(**config)

def get_series_id(name):
	with connection.cursor() as cursor:
		sql = 'select id from series where name=%s'
		cursor.execute(sql, (name))
		sid = cursor.fetchone()
		if sid:
			return sid[0]
		else:
			return None

class PinPaiSpiders(scrapy.Spider):
	name = 'new_series'
	start_urls=[
		'http://mcbd.maiche.com/api/open/v3/car-basic/get-new-car-serial-list.htm?_a=98v8vwz0V581wVz1zzV3119V68A27z355943&_appName=maichebaodian&_appUser=fdc59d78fa6ee9f6ad350a9a585840f9&_cityCode=110000&_cityName=%E5%8C%97%E4%BA%AC%E5%B8%82&_device=iPhone%207&_firstTime=2018-04-19%2021%3A24%3A37&_gpsType=ip&_html5=0&_imei=5de9d71345e4763cb1a14ed078e11456c54f00c4&_ipCity=110000&_j=1.0&_jail=false&_latitude=0&_launch=16&_longitude=0&_mac=5de9d71345e4763cb1a14ed078e11456c54f00c4&_manufacturer=Apple&_network=wifi&_operator=M&_pkgName=com.baojiazhijia.qichebaojia.maichewang&_platform=iphone&_product=%E4%B9%B0%E8%BD%A6%E5%AE%9D%E5%85%B8&_productCategory=qichebaojia&_r=cc923a01d0dcc45e8f1c18443084af05&_renyuan=mucang&_screenDip=2&_screenHeight=1334&_screenWidth=750&_system=iOS&_systemVersion=11.3&_u=9635v092V4081Vz651V6w41Vx63x9xAAx564&_vendor=appstore&_version=3.2.4&_webviewVersion=4.7&clientTimeMs=1526296025572&iosHardwareType=iPhone9%2C1&month=12&year=2017&sign=0046224d98151640a7bc08f4eb44fbc901',
		'http://mcbd.maiche.com/api/open/v3/car-basic/get-new-car-serial-list.htm?_a=98v8vwz0V581wVz1zzV3119V68A27z355943&_appName=maichebaodian&_appUser=fdc59d78fa6ee9f6ad350a9a585840f9&_cityCode=110000&_cityName=%E5%8C%97%E4%BA%AC%E5%B8%82&_device=iPhone%207&_firstTime=2018-04-19%2021%3A24%3A37&_gpsType=ip&_html5=0&_imei=5de9d71345e4763cb1a14ed078e11456c54f00c4&_ipCity=110000&_j=1.0&_jail=false&_latitude=0&_launch=16&_longitude=0&_mac=5de9d71345e4763cb1a14ed078e11456c54f00c4&_manufacturer=Apple&_network=wifi&_operator=M&_pkgName=com.baojiazhijia.qichebaojia.maichewang&_platform=iphone&_product=%E4%B9%B0%E8%BD%A6%E5%AE%9D%E5%85%B8&_productCategory=qichebaojia&_r=58e8047b3f8dc4d48455880aa0863acd&_renyuan=mucang&_screenDip=2&_screenHeight=1334&_screenWidth=750&_system=iOS&_systemVersion=11.3&_u=9635v092V4081Vz651V6w41Vx63x9xAAx564&_vendor=appstore&_version=3.2.4&_webviewVersion=4.7&clientTimeMs=1526296025583&iosHardwareType=iPhone9%2C1&month=5&year=2018&sign=33f09c4ef12441b2216288a41c7839e801',
		'http://mcbd.maiche.com/api/open/v3/car-basic/get-new-car-serial-list.htm?_a=98v8vwz0V581wVz1zzV3119V68A27z355943&_appName=maichebaodian&_appUser=fdc59d78fa6ee9f6ad350a9a585840f9&_cityCode=110000&_cityName=%E5%8C%97%E4%BA%AC%E5%B8%82&_device=iPhone%207&_firstTime=2018-04-19%2021%3A24%3A37&_gpsType=ip&_html5=0&_imei=5de9d71345e4763cb1a14ed078e11456c54f00c4&_ipCity=110000&_j=1.0&_jail=false&_latitude=0&_launch=16&_longitude=0&_mac=5de9d71345e4763cb1a14ed078e11456c54f00c4&_manufacturer=Apple&_network=wifi&_operator=M&_pkgName=com.baojiazhijia.qichebaojia.maichewang&_platform=iphone&_product=%E4%B9%B0%E8%BD%A6%E5%AE%9D%E5%85%B8&_productCategory=qichebaojia&_r=266591d9c47b33a82f139b26e6b495be&_renyuan=mucang&_screenDip=2&_screenHeight=1334&_screenWidth=750&_system=iOS&_systemVersion=11.3&_u=9635v092V4081Vz651V6w41Vx63x9xAAx564&_vendor=appstore&_version=3.2.4&_webviewVersion=4.7&clientTimeMs=1526296042865&iosHardwareType=iPhone9%2C1&month=1&year=2018&sign=1a95bf24d88425e39d75f61463d16c5901',
		'http://mcbd.maiche.com/api/open/v3/car-basic/get-new-car-serial-list.htm?_a=98v8vwz0V581wVz1zzV3119V68A27z355943&_appName=maichebaodian&_appUser=fdc59d78fa6ee9f6ad350a9a585840f9&_cityCode=110000&_cityName=%E5%8C%97%E4%BA%AC%E5%B8%82&_device=iPhone%207&_firstTime=2018-04-19%2021%3A24%3A37&_gpsType=ip&_html5=0&_imei=5de9d71345e4763cb1a14ed078e11456c54f00c4&_ipCity=110000&_j=1.0&_jail=false&_latitude=0&_launch=16&_longitude=0&_mac=5de9d71345e4763cb1a14ed078e11456c54f00c4&_manufacturer=Apple&_network=wifi&_operator=M&_pkgName=com.baojiazhijia.qichebaojia.maichewang&_platform=iphone&_product=%E4%B9%B0%E8%BD%A6%E5%AE%9D%E5%85%B8&_productCategory=qichebaojia&_r=1fd932e2acc36b70822cf2c80f4db4eb&_renyuan=mucang&_screenDip=2&_screenHeight=1334&_screenWidth=750&_system=iOS&_systemVersion=11.3&_u=9635v092V4081Vz651V6w41Vx63x9xAAx564&_vendor=appstore&_version=3.2.4&_webviewVersion=4.7&clientTimeMs=1526296043990&iosHardwareType=iPhone9%2C1&month=2&year=2018&sign=817b7243a9d817ba57ab379e1ee3055201',
		'http://mcbd.maiche.com/api/open/v3/car-basic/get-new-car-serial-list.htm?_a=98v8vwz0V581wVz1zzV3119V68A27z355943&_appName=maichebaodian&_appUser=fdc59d78fa6ee9f6ad350a9a585840f9&_cityCode=110000&_cityName=%E5%8C%97%E4%BA%AC%E5%B8%82&_device=iPhone%207&_firstTime=2018-04-19%2021%3A24%3A37&_gpsType=ip&_html5=0&_imei=5de9d71345e4763cb1a14ed078e11456c54f00c4&_ipCity=110000&_j=1.0&_jail=false&_latitude=0&_launch=16&_longitude=0&_mac=5de9d71345e4763cb1a14ed078e11456c54f00c4&_manufacturer=Apple&_network=wifi&_operator=M&_pkgName=com.baojiazhijia.qichebaojia.maichewang&_platform=iphone&_product=%E4%B9%B0%E8%BD%A6%E5%AE%9D%E5%85%B8&_productCategory=qichebaojia&_r=e127b7f1115cc305a47a33572622dcb1&_renyuan=mucang&_screenDip=2&_screenHeight=1334&_screenWidth=750&_system=iOS&_systemVersion=11.3&_u=9635v092V4081Vz651V6w41Vx63x9xAAx564&_vendor=appstore&_version=3.2.4&_webviewVersion=4.7&clientTimeMs=1526296044740&iosHardwareType=iPhone9%2C1&month=3&year=2018&sign=fc5231e35cfcef775acbac970a5369bf01',
		'http://mcbd.maiche.com/api/open/v3/car-basic/get-new-car-serial-list.htm?_a=98v8vwz0V581wVz1zzV3119V68A27z355943&_appName=maichebaodian&_appUser=fdc59d78fa6ee9f6ad350a9a585840f9&_cityCode=110000&_cityName=%E5%8C%97%E4%BA%AC%E5%B8%82&_device=iPhone%207&_firstTime=2018-04-19%2021%3A24%3A37&_gpsType=ip&_html5=0&_imei=5de9d71345e4763cb1a14ed078e11456c54f00c4&_ipCity=110000&_j=1.0&_jail=false&_latitude=0&_launch=16&_longitude=0&_mac=5de9d71345e4763cb1a14ed078e11456c54f00c4&_manufacturer=Apple&_network=wifi&_operator=M&_pkgName=com.baojiazhijia.qichebaojia.maichewang&_platform=iphone&_product=%E4%B9%B0%E8%BD%A6%E5%AE%9D%E5%85%B8&_productCategory=qichebaojia&_r=e0592da5db690a30bd00f3987ce71153&_renyuan=mucang&_screenDip=2&_screenHeight=1334&_screenWidth=750&_system=iOS&_systemVersion=11.3&_u=9635v092V4081Vz651V6w41Vx63x9xAAx564&_vendor=appstore&_version=3.2.4&_webviewVersion=4.7&clientTimeMs=1526296045488&iosHardwareType=iPhone9%2C1&month=4&year=2018&sign=38ae25f4e1cf9d6c9adbec1b406a05db01',
		'http://mcbd.maiche.com/api/open/v3/car-basic/get-new-car-serial-list.htm?_a=98v8vwz0V581wVz1zzV3119V68A27z355943&_appName=maichebaodian&_appUser=fdc59d78fa6ee9f6ad350a9a585840f9&_cityCode=110000&_cityName=%E5%8C%97%E4%BA%AC%E5%B8%82&_device=iPhone%207&_firstTime=2018-04-19%2021%3A24%3A37&_gpsType=ip&_html5=0&_imei=5de9d71345e4763cb1a14ed078e11456c54f00c4&_ipCity=110000&_j=1.0&_jail=false&_latitude=0&_launch=16&_longitude=0&_mac=5de9d71345e4763cb1a14ed078e11456c54f00c4&_manufacturer=Apple&_network=wifi&_operator=M&_pkgName=com.baojiazhijia.qichebaojia.maichewang&_platform=iphone&_product=%E4%B9%B0%E8%BD%A6%E5%AE%9D%E5%85%B8&_productCategory=qichebaojia&_r=28e64a78b43ef0734f0253d58c7f6d10&_renyuan=mucang&_screenDip=2&_screenHeight=1334&_screenWidth=750&_system=iOS&_systemVersion=11.3&_u=9635v092V4081Vz651V6w41Vx63x9xAAx564&_vendor=appstore&_version=3.2.4&_webviewVersion=4.7&clientTimeMs=1526296048401&iosHardwareType=iPhone9%2C1&month=6&year=2018&sign=345b1071efe69e055ecf7e297835cbe601',
	]
	

	def parse(self, response):
		res = json.loads(response.text)
		series_list = res['data']
		url = response.url
		month = url[url.find('month')+6:url.find('&year')]
		if len(month) < 2:
			month = '0' + month
		year = url[url.find('year')+5:url.find('&sign')]
		for k in series_list:
			item = items.GetNewCarsItem()
			up_at = k['listedTime']
			series = k['serial']
			item['series_id'] = None
			item['name'] = series.get('name', '')
			item['series_id'] = get_series_id(item['name'])
			item['img_url'] = series.get('imageUrl', '')[:-6]
			item['sale_at'] = year + month
			item['ntype'] = k['upgradeType']
			item['maxprice'] = series.get('maxPrice', '0')
			item['minprice'] = series.get('minPrice', '0')
			print(item)
			yield item

		