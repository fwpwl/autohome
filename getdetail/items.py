# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import pymysql


class GetdetailItem(scrapy.Item):
	id = scrapy.Field()
	grade = scrapy.Field()
	maxprice = scrapy.Field()
	minprice = scrapy.Field()
	d_url = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "update `series` set maxprice=%s, grade=%s, minprice=%s, d_url=%s where id=%s"
				data = (self.get('maxprice', ''), self.get('grade', ''), self.get('minprice', ''), self.get('d_url', ''), self.get('id', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("update series fail %s" % e)


class GetPriceItem(scrapy.Item):
	car_id = scrapy.Field()
	series_id = scrapy.Field()
	ori_price = scrapy.Field()
	per_price = scrapy.Field()
	d_price = scrapy.Field()
	dealer_id = scrapy.Field()
	city = scrapy.Field()
	stock = scrapy.Field()
	city_id = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into cut_price(car_id, series_id, ori_price, per_price, d_price, city, dealer_id, stock, city_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
				data = (self.get('car_id', ''), self.get('series_id', ''), str(self.get('ori_price', '')), self.get('per_price', ''), self.get('d_price', ''), self.get('city', ''), self.get('dealer_id', ''), self.get('stock', ''), self.get('city_id', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save cut_prices fail %s" % e)


class GetSeriesItem(scrapy.Item):
	id = scrapy.Field()
	name = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into d_series(id, name) values(%s, %s)"
				data = (self.get('id', ''), self.get('name', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save d_series fail %s" % e)

class ColumnsItem(scrapy.Item):
	name = scrapy.Field()
	items = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into columns(name, items) values(%s, %s)"
				data = (self.get('name', ''), self.get('items', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save columns fail %s" % e)


class SpecItem(scrapy.Item):
	id = scrapy.Field()
	series_id = scrapy.Field()
	i1 = scrapy.Field()
	i2 = scrapy.Field()
	i3 = scrapy.Field()
	i4 = scrapy.Field()
	i5 = scrapy.Field()
	i6 = scrapy.Field()
	i7 = scrapy.Field()
	i8 = scrapy.Field()
	i9 = scrapy.Field()
	i10 = scrapy.Field()
	i11 = scrapy.Field()
	i12 = scrapy.Field()
	i13 = scrapy.Field()
	i14 = scrapy.Field()
	i15 = scrapy.Field()
	i16 = scrapy.Field()
	i17 = scrapy.Field()
	i18 = scrapy.Field()
	i19 = scrapy.Field()
	i20 = scrapy.Field()
	config = scrapy.Field()
	i300 = scrapy.Field()
	i301 = scrapy.Field()
	i302 = scrapy.Field()
	i303 = scrapy.Field()
	i304 = scrapy.Field()
	i305 = scrapy.Field()
	i306 = scrapy.Field()
	i307 = scrapy.Field()
	i308 = scrapy.Field()
	i309 = scrapy.Field()
	i310 = scrapy.Field()
	i311 = scrapy.Field()
	i312 = scrapy.Field()
	i313 = scrapy.Field()
	i314 = scrapy.Field()
	i315 = scrapy.Field()
	i316 = scrapy.Field()
	i317 = scrapy.Field()
	i318 = scrapy.Field()
	i319 = scrapy.Field()
	i320 = scrapy.Field()
	i321 = scrapy.Field()
	i322 = scrapy.Field()

	def saveto_mysql(self, db):
		id = int(self.get('id', 0))
		series_id = self.get('series_id', None)
		i1 = self.get('i1', '')
		i2 = self.get('i2', '')
		i3 = self.get('i3', '')
		i4 = self.get('i4', '')
		i5 = self.get('i5', '')
		i6 = self.get('i6', '')
		i7 = self.get('i7', '')
		i8 = self.get('i8', '')
		i9 = self.get('i9', '')
		i10 = self.get('i10', '')
		i11 = self.get('i11', '')
		i12 = self.get('i12', '')
		i13 = self.get('i13', '')
		i14 = self.get('i14', '')
		i15 = self.get('i15', '')
		i16 = self.get('i16', '')
		i17 = self.get('i17', '')
		i18 = self.get('i18', '')
		i19 = self.get('i19', '')
		i20 = self.get('i20', '')
		config = self.get('config', '')
		i300 = float(self.get('i300', '0'))
		i301 = int(self.get('i301', '0'))
		i302 = self.get('i302', '')
		i303 = int(self.get('i303', '0'))
		i304 = int(self.get('i304', '0'))
		i305 = int(self.get('i305', '0'))
		i306 = int(self.get('i306', '0'))
		i307 = int(self.get('i307', '0'))
		i308 = int(self.get('i308', '0'))
		i309 = int(self.get('i309', '0'))
		i310 = int(self.get('i310', '0'))
		i311 = int(self.get('i311', '0'))
		i312 = int(self.get('i312', '0'))
		i313 = int(self.get('i313', '0'))
		i314 = int(self.get('i314', '0'))
		i315 = int(self.get('i315', '0'))
		i316 = int(self.get('i316', '0'))
		i317 = int(self.get('i317', '0'))
		i318 = int(self.get('i318', '0'))
		i319 = int(self.get('i319', '0'))
		i320 = int(self.get('i320', '0'))
		i321 = int(self.get('i321', '0'))
		i322 = int(self.get('i322', '0'))
		try:
			with db.cursor() as cursor:
				sql = "INSERT INTO `specs` (`id`,`series_id`,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19,i20,config,i300,i301,i302,i303,i304,i305,i306,i307,i308,i309,i310,i311,i312,i313,i314,i315,i316,i317,i318,i319,i320,i321,i322) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				data = (id, series_id, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16,i17,i18,i19,i20,config,i300,i301,i302,i303,i304,i305,i306,i307,i308,i309,i310,i311,i312,i313,i314,i315,i316,i317,i318,i319,i320,i321,i322)
				cursor.execute(sql, data)
				db.commit()
		except Exception as e:
			print("save specs fail %s" % e)


class DealersItem(scrapy.Item):
	id = scrapy.Field()
	name = scrapy.Field()
	address = scrapy.Field()
	sell_phone = scrapy.Field()
	sale_range = scrapy.Field()
	sale_to = scrapy.Field()
	company = scrapy.Field()
	province_id = scrapy.Field()
	city_id = scrapy.Field()
	county_id = scrapy.Field()
	contacts = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into dealers(id, name, address, sell_phone, sale_range, sale_to, company, province_id, city_id, county_id, contacts) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				data = (self.get('id', ''), self.get('name', ''), self.get('address', ''), self.get('sell_phone', ''), self.get('sale_range', ''), self.get('sale_to', ''),self.get('company', ''),self.get('province_id', ''),self.get('city_id', ''),self.get('county_id', ''), self.get('contacts', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save dealers fail %s" % e)


class GetArticlesItem(scrapy.Item):
	title = scrapy.Field()
	t_url = scrapy.Field()
	author = scrapy.Field()
	comment = scrapy.Field()

	def saveto_mysql(self, db):
		title = self.get('title', '')
		t_url = self.get('t_url', '')
		author = self.get('author', '')
		comment = self.get('comment', '')
		try:
			with db.cursor() as cursor:
				sql = "insert into art_recommends(title, t_url, author,comment) values("'"%s"'","'"%s"'","'"%s"'","'"%s"'")"
				data = (pymysql.escape_string(title), pymysql.escape_string(t_url), pymysql.escape_string(author), pymysql.escape_string(comment))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("insert art_recommends fail %s" % e)


class ImgItem(scrapy.Item):
	url = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into images(url) values(%s)"
				data = (self.get('url', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save img fail %s" % e)


class DealerItem(scrapy.Item):
	id = scrapy.Field()
	series_id = scrapy.Field()
	name = scrapy.Field()
	company = scrapy.Field()
	address = scrapy.Field()
	province_id = scrapy.Field()
	city_id = scrapy.Field()
	county_id = scrapy.Field()
	saleto = scrapy.Field()
	lon = scrapy.Field()
	lat = scrapy.Field()
	contacts = scrapy.Field()
	sellphone = scrapy.Field()
	maxprice = scrapy.Field()
	minprice = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into dealer(id, series_id, name, company, address,province_id, city_id, county_id,saleto,lon,lat,contacts,sellphone,maxprice,minprice) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
				data = (self.get('id', ''), self.get('series_id', ''),self.get('name', ''),self.get('company', ''),self.get('address', ''),self.get('province_id', ''),self.get('city_id', ''),self.get('county_id', ''), self.get('saleto', ''),self.get('lon', ''),self.get('lat', ''),self.get('contacts', ''),self.get('sellphone', ''), self.get('maxprice', ''),self.get('minprice', ''),)
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save img fail %s" % e)


class ScoreItem(scrapy.Item):
	series_id = scrapy.Field()
	score = scrapy.Field()
	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into public_praise_score(series_id, score) values(%s, %s)"
				data = (self.get('series_id', ''), self.get('score', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save img fail %s" % e)


class PraiseNumItem(scrapy.Item):
	id = scrapy.Field()
	praise_num = scrapy.Field()
	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into series_praise_num(id, praise_num) values(%s, %s)"
				data = (self.get('id', ''), self.get('praise_num', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save img fail %s" % e)


class BaodianItem(scrapy.Item):
	series_id = scrapy.Field()
	name = scrapy.Field()
	url = scrapy.Field()
	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into baodian_360(series_id, name, url) values(%s, %s, %s)"
				data = (self.get('series_id', ''), self.get('name', ''), self.get('url', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save img fail %s" % e)


class GetNewCarsItem(scrapy.Item):
	series_id = scrapy.Field()
	name = scrapy.Field()
	img_url = scrapy.Field()
	sale_at = scrapy.Field()
	ntype = scrapy.Field()
	price = scrapy.Field()
	level = scrapy.Field()
	images_urls = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into new_series(series_id, name, img_url, sale_at, ntype, price,level) values(%s, %s,%s, %s, %s,%s,%s)"
				data = (self.get('series_id', ''), self.get('name', ''), self.get('img_url', ''),self.get('sale_at', ''),self.get('ntype', ''),self.get('price', ''), self.get('level', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save img fail %s" % e)


class CheZhuZhiJiaItem(scrapy.Item):
	name = scrapy.Field()
	address = scrapy.Field()
	phone = scrapy.Field()
	dtype = scrapy.Field()
	url = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into chezhuzhijia2(name, address, phone, dtype, url) values(%s,%s,%s,%s,%s)"
				data = ( self.get('name', ''), self.get('address', ''),self.get('phone', ''),self.get('dtype', ''),self.get('url', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save img fail %s" % e)


class DealerLoctionItem(scrapy.Item):
	id = scrapy.Field()
	province_id = scrapy.Field()
	city_id = scrapy.Field()
	sid = scrapy.Field()
	loc = scrapy.Field()
	lon = scrapy.Field()
	lat = scrapy.Field()

	def saveto_mysql(self, db):
		try:
			with db.cursor() as cursor:
				sql = "insert into cyx.dealer_location(id, province_id, city_id, sid, loc, lon, lat) values(%s,%s,%s,%s,ST_PointFromText(%s),%s,%s)"
				data = ( self.get('id', ''), self.get('province_id', ''),self.get('city_id', ''),self.get('sid', ''),self.get('loc', ''), self.get('lon', ''),self.get('lat', ''))
				cursor.execute(sql, data)
			db.commit()
		except Exception as e:
			print("save img fail %s" % e)
