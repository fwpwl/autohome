# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors
from scrapy.exceptions import DropItem
from getdetail import items
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import shutil
from scrapy.utils.project import get_project_settings
import os

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class GetDetailPipeline(object):
	def __init__(self, dbparams):
		self.dbparams = dbparams

	@classmethod
	def from_crawler(cls, crawler):
		dbparams=dict(
						host=crawler.settings['MYSQL_HOST'],
						db=crawler.settings['MYSQL_DBNAME'],
						user=crawler.settings['MYSQL_USER'],
						passwd=crawler.settings['MYSQL_PASSWD'],
						charset='utf8',
						cursorclass=pymysql.cursors.DictCursor,
						use_unicode=False,
				)

		return cls(
				dbparams=dbparams,
				)

	#spider开启时，该方法被执行，连接数据库
	def open_spider(self, spider):
		self.connection = pymysql.connect(**self.dbparams)

	#spider关闭时，该方法被执行
	def close_spider(self, spider):
		self.connection.close()

	def process_item(self, item, spider):
		if hasattr(item, "saveto_mysql"):
			if callable(item.saveto_mysql):
				item.saveto_mysql(self.connection)
		return item


class ImageDownloadPipeline(ImagesPipeline):
	
	img_store = get_project_settings().get('IMAGES_STORE')

	def get_media_requests(self, item, info):
		if item.get('img_url'):
			for image_url in [item['img_url']]:
				yield Request(image_url)

	def item_completed(self, results, item, info):
		
		img_path = "%s%s"%(self.img_store, item['sale_at'])

		if os.path.exists(img_path) == False:
			os.mkdir(img_path)
		
		for key,value in results:
			image_file_path = value['path']
			img_name = image_file_path.split('/')[-1]
			
			shutil.move(self.img_store + image_file_path, img_path + "/" + img_name)
		site = 'http://cdn.autoforce.net/cyx/images/new_series/' + item['sale_at'] + '/'
		item['img_url'] = site + image_file_path.split('/')[-1]
		return item
			
