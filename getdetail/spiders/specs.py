# -*- coding: utf-8 -*-

import scrapy
import string
from getdetail import items
import re
import json
from scrapy.http import Request
import pymysql.cursors
from bloom_filter import BloomFilter


config = {
          'host': '192.168.10.100',
          'port': 3306,
          'user': 'afsaas',
          'password': '218F2AE2-F275-430B-A20B-1FD9E0CAD419',
          'db': 'cyx',
          'charset': 'utf8mb4',
        }
connection = pymysql.connect(**config)

# def get_car_id(id):
#     try:
#         with connection.cursor() as cursor:
#             sql = "select id from specs where id=%s"
#             cursor.execute(sql, (id))
#             id = cursor.fetchone()
#             if id:
#                 print('result', id)
#                 return id[0]
#             else:
#                 return None
#     except Exception as e:
#         return None

def get_column_id(name):
    config_dict = {'220V/230V电源': 165,
 'ABS防抱死': 78,
 'CD/DVD': 167,
 'GPS导航系统': 155,
 'HUD抬头数字显示': 131,
 'ISOFIX儿童座椅接口': 77,
 'LED日间行车灯': 172,
 '上坡辅助': 96,
 '上市时间': 6,
 '中央差速器锁止功能': 104,
 '中控台彩色大屏': 157,
 '中控台彩色大屏尺寸': 158,
 '中控液晶屏分屏显示': 159,
 '主/副驾驶座安全气囊': 70,
 '主/副驾驶座电动调节': 140,
 '主动刹车/主动安全系统': 85,
 '主动降噪': 133,
 '供油方式': 52,
 '侧滑门': 112,
 '倒车视频影像': 89,
 '全景天窗': 108,
 '全景摄像头': 90,
 '全液晶仪表盘': 130,
 '内/外后视镜自动防眩目': 187,
 '内置行车记录仪': 132,
 '制动力分配(EBD/CBC等)': 79,
 '刹车辅助(EBA/BAS/BA等)': 80,
 '前/后中央扶手': 152,
 '前/后排侧气囊': 71,
 '前/后排头部气囊(气帘)': 72,
 '前/后排座椅加热': 146,
 '前/后排座椅按摩': 148,
 '前/后排座椅通风': 147,
 '前/后电动车窗': 181,
 '前/后驻车雷达': 88,
 '前制动器类型': 64,
 '前悬架类型': 60,
 '前桥限滑差速器/差速锁': 103,
 '前轮胎规格': 67,
 '前轮距(mm)': 25,
 '前雾灯': 177,
 '副驾驶位后排可调节按钮': 144,
 '助力类型': 62,
 '厂商': 3,
 '厂商指导价(元)': 2,
 '压缩比': 40,
 '发动机': 9,
 '发动机启停技术': 94,
 '发动机型号': 34,
 '发动机特有技术': 49,
 '发动机电子防盗': 116,
 '变速箱': 10,
 '变速箱类型': 57,
 '可加热/制冷杯架': 154,
 '可变悬架': 99,
 '可变转向比': 102,
 '后制动器类型': 65,
 '后座出风口': 199,
 '后悬架类型': 61,
 '后排侧遮阳帘': 192,
 '后排侧隐私玻璃': 193,
 '后排座椅放倒方式': 151,
 '后排座椅电动调节': 143,
 '后排杯架': 153,
 '后排液晶屏': 164,
 '后排独立空调': 198,
 '后桥限滑差速器/差速锁': 105,
 '后视镜加热': 186,
 '后视镜电动折叠': 189,
 '后视镜电动调节': 185,
 '后视镜记忆': 190,
 '后轮胎规格': 68,
 '后轮距(mm)': 26,
 '后雨刷': 195,
 '后风挡遮阳帘': 191,
 '备胎规格': 69,
 '外接音源接口': 166,
 '多功能方向盘': 125,
 '夜视系统': 86,
 '大灯清洗装置': 179,
 '大灯高度可调': 178,
 '安全带未系提示': 76,
 '官方0-100km/h加速(s)': 14,
 '定位互动服务': 156,
 '定速巡航': 91,
 '实测0-100km/h加速(s)': 15,
 '实测100-0km/h制动(m)': 16,
 '实测油耗(L/100km)': 19,
 '实测离地间隙(mm)': 17,
 '宽度(mm)': 22,
 '工信部综合油耗(L/100km)': 18,
 '并线辅助': 83,
 '座位数(个)': 30,
 '座椅材质': 135,
 '座椅高低调节': 137,
 '感应后备厢': 114,
 '感应雨刷': 196,
 '手机互联/映射': 161,
 '手机无线充电': 134,
 '扬声器品牌': 168,
 '扬声器数量': 169,
 '挡位个数': 56,
 '排量(mL)': 35,
 '整体主动转向系统': 106,
 '整备质量(kg)': 33,
 '整车质保': 20,
 '方向盘加热': 127,
 '方向盘换挡': 126,
 '方向盘电动调节': 124,
 '方向盘记忆': 128,
 '方向盘调节': 123,
 '无钥匙启动系统': 119,
 '无钥匙进入系统': 120,
 '最大功率(kW)': 45,
 '最大功率转速(rpm)': 46,
 '最大扭矩(N·m)': 47,
 '最大扭矩转速(rpm)': 48,
 '最大马力(Ps)': 44,
 '最小离地间隙(mm)': 27,
 '最高车速(km/h)': 13,
 '每缸气门数(个)': 39,
 '气缸排列形式': 37,
 '气缸数(个)': 38,
 '油箱容积(L)': 31,
 '流媒体车内后视镜': 188,
 '温度分区控制': 200,
 '燃料形式': 50,
 '燃油标号': 51,
 '牵引力控制(ASR/TCS/TRC等)': 81,
 '环保标准': 55,
 '电动后备厢': 113,
 '电动吸合门': 111,
 '电动天窗': 107,
 '电动座椅记忆': 145,
 '电磁感应悬架': 101,
 '疲劳驾驶提示': 87,
 '皮质方向盘': 122,
 '空气悬架': 100,
 '空调控制方式': 197,
 '第三排座椅': 150,
 '第二排座椅移动': 142,
 '第二排独立座椅': 149,
 '第二排靠背角度调节': 141,
 '简称': 58,
 '级别': 4,
 '缸体材料': 54,
 '缸径(mm)': 42,
 '缸盖材料': 53,
 '肩部支撑调节': 139,
 '胎压监测装置': 74,
 '能源类型': 5,
 '腰部支撑调节': 138,
 '膝部气囊': 73,
 '自动头灯': 174,
 '自动泊车入位': 93,
 '自动驻车': 97,
 '自动驾驶技术': 95,
 '自适应巡航': 92,
 '自适应远近光': 173,
 '蓝牙/车载电话': 160,
 '行李厢容积(L)': 32,
 '行程(mm)': 43,
 '行车电脑显示屏': 129,
 '车体结构': 63,
 '车内中控锁': 117,
 '车内氛围灯': 180,
 '车内空气调节/花粉过滤': 201,
 '车型名称': 1,
 '车窗一键升降': 182,
 '车窗防夹手功能': 183,
 '车联网': 162,
 '车身稳定控制(ESC/ESP/DSC等)': 82,
 '车身结构': 28,
 '车载冰箱': 203,
 '车载电视': 163,
 '车载空气净化器': 202,
 '车道偏离预警系统': 84,
 '车门数(个)': 29,
 '车顶行李架': 115,
 '转向头灯': 176,
 '转向辅助灯': 175,
 '轴距(mm)': 24,
 '运动外观套件': 109,
 '运动风格座椅': 136,
 '近光灯': 170,
 '进气形式': 36,
 '远光灯': 171,
 '远程启动': 121,
 '遥控钥匙': 118,
 '遮阳板化妆镜': 194,
 '配气机构': 41,
 '铝合金轮圈': 110,
 '长*宽*高(mm)': 11,
 '长度(mm)': 21,
 '防紫外线/隔热玻璃': 184,
 '陡坡缓降': 98,
 '零胎压继续行驶': 75,
 '驱动方式': 59,
 '驻车制动类型': 66,
 '高度(mm)': 23}
 
    return config_dict.get(name, None)

class SpecsSpider(scrapy.Spider):
        name = "autohome_specs1"
        start_urls = ['https://car.m.autohome.com.cn/']

        def __init__(self):
            self.filename = "ids.bf"
            self.ids = BloomFilter(max_elements=10000000, error_rate=0.001, filename=self.filename)

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
                if id not in self.ids:
                    self.ids.add(id)
                    yield Request('https://car.m.autohome.com.cn/ashx/car/GetModelConfig.ashx?ids=%s'% id, meta={'car_id': id, 'series_id': series_id}, callback=self.parse_spec)
                print('%s 在ids'%id)

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
                    columns_dict['i' + str(id)] = v
            item['id'] = int(response.meta['car_id'])
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
