#coding=utf-8

import pymysql.cursors
import sys
import os
import urllib.request
import time


config = {
		  'host':'127.0.0.1',
		  'port':3306,
		  'user':'root',
		  'password':'',
		  'db':'cyx',
		  'charset':'utf8mb4',
		  }
connection = pymysql.connect(**config)

def save_img(img_url,file_name,file_path):
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        filename = '{}{}{}'.format(file_path,os.sep,file_name)
        urllib.request.urlretrieve(img_url, filename=filename)
    except Exception as e:
        print(e)

try:
	with connection.cursor() as cursor:
		sql = 'select * from art_recommends'
		cursor.execute(sql)
		res = cursor.fetchall()
		if res:
			for k in res:
				url = 'http://cdn.autoforce.net/cyx/images/recommends/'
				name = url + k[2].split('/')[-1]
				print('update cyx.art_recommends set t_url='"'%s'"' where id=%s'%(name, k[0]) + ';')
				# save_img(url, name, './images')
finally:
	connection.close()