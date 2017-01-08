# -*- coding: utf-8 -*-
import happybase as hb
import random as rd
import numpy as np

class hbAccess:

	def __init__(self):
		#happyBase specification
		self.hbServer = "localhost"
		self.hbPort = 9090
		self.tableName = "OLPOWERINFO"
		self.maxRow =  54719418
		self.testMinRow = 54719419
		self.testMaxRow = 109438836
		#Set label dictionary
		self.diction = dict({b"UNKNOWN": 0,b"筆電": 1,b"電腦": 2,b"冷氣": 3,b"冰箱": 4,b"熱水瓶": 5,b"除濕機": 6,b"電鍋": 7,b"電熱水器": 8,b"洗衣機": 9,b"電視": 10,b"音響": 11,b"無線網路分享器": 12,b"PS3": 13,b"天線": 14,b"播放器": 15,b"Wii 遊戲機": 16,b"水族箱": 17,b"電風扇": 18,b"檯燈": 19,b"電燈": 20,b"飲水機": 21,b"跑步機": 22,b"螢幕": 23,b"淨水器": 24,b"充電器": 25,b"微波爐": 26,b"烤箱": 27,b"電磁爐": 28,b"數據機": 29,b"烘乾機": 30,b"氣炸鍋": 31,b"手機充電器": 32,b"電話": 33,b"電池充電器": 34,b"吸塵器": 35,b"鬆餅機": 36,b"魚缸燈": 37,b"咖啡機": 38,b"數位機上盒": 39,b"平板充電櫃": 40,b"電子鍋": 41,b"MOD機上盒": 42,b"卡拉OK": 43,b"空氣清淨機": 44,b"插座": 45,b"消毒鍋": 46,b"總電表": 47,b"電暖器": 48,b"手機充電頭": 49,b"印表機": 50,b"媒體撥放器": 51,b"馬達": 52,b"黑晶爐": 53,b"烤吐司機": 54,b"魚缸過濾器": 55,b"吹風機": 56,b"機上盒": 57,b"烘碗機": 58,b"燈": 59,b"XBOX": 60,b"按摩椅": 61,b"果汁機": 62,b"備用插座": 63,b"烘衣機": 64,b"網路設備": 65,b"路由器": 66,b"防潮箱": 67,b"NAS": 68,b"電子鐘": 69,b"監視錄影機": 70,b"監視器": 71,b"延長線": 72,b"MOD寬頻數據機": 73,b"魚缸": 74,b"滅蚊燈": 75,b"擴大機": 76,b"快煮壺": 77,b"閘道器": 78,b"奶瓶消毒鍋": 79,b"網路電視盒": 80,b"電熨斗": 81,b"溫濕度計": 82,b"抽風機": 83,b"溫溼度計": 84,b"電視機上盒": 85,b"抽油煙機": 86,b"熱水器": 87,b"電腦排插": 88,b"縫紉機": 89,b"分享器": 90,b"平板充電器": 91,b"冷凍櫃": 92,b"IP Cam": 93,b"掃地機器人": 94,b"吸塵器 吹風機": 95,b"伺服器": 96,b"USB 充電器": 97,b"燈炮": 98,b"電熱壺": 99,b"音響擴大機": 100,b"家庭劇院": 101,b"電動牙刷": 102,b"手機充電座": 103,b"麵包機": 104,b"Google眼鏡": 105,b"IP 分享器": 106,b"捕蚊燈": 107,b"幫浦": 108,b"補蚊燈": 109,b"硬碟": 110,b"視訊機": 111,b"平板電腦": 112,b"神桌燈": 113,b"優格機": 114,b"風扇": 115,b"魚缸加溫器": 116,b"製麵機": 117,b"強波器": 118,b"無線電話": 119,b"蒸奶器": 120,b"魚缸照明": 121,b"外接式硬碟": 122,b"免治馬桶座": 123,b"無線網路基地台": 124,b"充電座": 125,b"霧化扇": 126,b"電蚊香": 127,b"電蚊燈": 128,b"UPS": 129,b"主機": 130,b"小夜燈": 131,b"MOD 分享器": 132,b"奶瓶消毒機": 133,b"多功能插座": 134,b"暖氣": 135,b"網路分享器": 136,b"感應器": 137,b"薰香燈": 138,b"抽水馬達": 139,b"打氣機": 140,b"殺菌燈": 141,b"加熱器": 142,b"寬頻分享器": 143,b"攝影機": 144,b"電子磅秤": 145,b"溫度計": 146,b"鍋具": 147,b"冷水機": 148,b"基地台": 149,b"全電器": 150,b"魚缸濾水器": 151,b"集線器": 152,b"排插": 153,b"加壓馬達": 154,b"總電器": 155,b"網路交換器": 156,b"喇叭": 157,b"過濾器": 158,b"保溫器": 159,b"分離式冷氣": 160,b"網路系統": 161,b"洗碗機": 162,b"暖爐": 163,b"電子溫度計": 164,b"VHS播放器": 165,b"太陽能發電": 166,b"網路電視": 167,b"電鑽": 168,b"快熱壺": 169,b"充電區": 170,b"佛桌小燈": 171,b"電子琴": 172,b"加溫器": 173,b"收音機": 174,b"鹽燈": 175,b"熱敷墊": 176,b"充電櫃": 177,b"逆變器": 178,b"真空管": 179,b"投影機": 180,b"料理鍋": 181,b"電子白板": 182,b"電熱器": 183,b"調乳器": 184,b"流水盆": 185,b"電動機車充電器": 186,b"視聽組": 187,b"數位天線": 188,b"單槍投影機": 189,b"監測": 190,b"萬用鍋": 191,b"製包子機": 192,b"影音設備": 193,b"電視遊樂器 Wii": 194,b"溫奶器": 195,b"電動按摩器": 196,b"豆漿機": 197,b"煎藥機": 198,b"洗機機": 199,b"蒸鍋": 200,b"雙溫控烤箱": 201,b"智慧燈具": 202,b"馬桶座": 203,b"電膜電暖器": 204,b"分離式冷氣子機": 205,b"多媒體播放機": 206,b"馬桶": 207,b"按摩器": 208,b"網路攝影機": 209,b"熨斗": 210,b"烤腳機": 211,b"選台器": 212,b"勳風循環扇": 213,b"吸乳器": 214,b"水族箱馬達": 215,b"循環扇": 216,b"雞蛋糕機": 217,b"擠乳器": 218,b"抽水機": 219,b"電熱毯": 220,b"磁場看板": 221,b"客電視": 222,b"電力橋接器": 223,b"加熱床": 224,b"監視攝影機": 225,b"電視錄影機": 226,b"磨豆機": 227,b"螢幕螢幕": 228,b"影音切換器": 229,b"光碟機": 230,b"無線網路機第台": 231})
		self.diction.update({b"血壓計": 232,b"防潮棒": 233,b"貓咪飲水機": 234,b"壓力鍋": 235,b"視訊盒": 236,b"SWITCH": 237,b"排油煙機": 238,b"傳真機": 239,b"車牌攝影機": 240,b"車充": 241,b"網路電源": 242,b"影印機": 243,b"電視強波器": 244,b"行動電源": 245,b"照明": 246,b"網路電話設備": 247,b"列表機": 248,b"烘奶瓶": 249,b"除濕棒": 250,b"多媒體播放器": 251,b"網路機上盒": 252,b"魚缸幫浦": 253,b"移動式冷氣": 254,b"真空管擴大機": 255,b"霧化器": 256,b"網路數據機": 257,b"水冷扇": 258,b"行動裝置充電器": 259,b"功率放大器": 260,b"VOD": 261,b"飲水器": 262,b"燈泡": 263,b"碎紙機": 264,b"電動刮鬍刀": 265,b"交換器": 266,b"刮鬍刀": 267,b"藍光播放器": 268,b"計時器": 269,b"感應": 270,b"烤麵包機": 271,b"網通裝置": 272,b"MOD 數據機": 273,b"數位錄影機": 274,b"XBOX 播放器": 275,b"開飲機": 276,b"數位轉換器": 277,b"影音設備 電扇": 278,b"充電組": 279,b"錄影機": 280,b"煎藥壺": 281,b"隨身聽": 282,b"變壓器": 283,b"掃描器": 284,b"水族箱換水裝置": 285,b"後電鍋": 286,b"變電器": 287,b"燈具": 288,b"捕蚊器": 289,b"奶瓶烘乾機": 290,b"電力網": 291,b"蒸爐": 292,b"乾燥機": 293,b"螢幕變壓器": 294,b"緊急照明燈": 295,b"攪拌器": 296,b"水族箱CO2": 297,b"噴水馬達": 298,b"鹽燈 XBOX": 299,b"煮水壺": 300,b"綠能控制器": 301,b"高畫質接收機": 302,b"監控攝影機": 303,b"雲端智慧盒": 304,b"精油燈": 305,b"水族箱過瀘器": 306,b"筆電變壓器": 307,b"換片機": 308,b"孔雀": 309,b"沖洗馬桶": 310,b"藍牙接收器": 311,b"發電機": 312,b"播放機": 313,b"時鐘": 314,b"魚缸打氣機": 315,b"咖啡壺": 316,b"海水馬達": 317,b"電視遊樂器 PS3": 318,b"監視器主機": 319,b"溫水器": 320,b"智慧型馬桶": 321,b"電陶爐": 322,b"數位電視天線": 323,b"冰櫃": 324,b"開發板": 325,b"交換機": 326,b"麥克風": 327,b"伴唱機": 328,b"水閥": 329,b"相機充電器": 330,b"鋼琴": 331,b"遠紅外線治療儀": 332,b"桌機": 333,b"水氧機": 334,b"耶誕燈": 335,b"掃地機": 336,b"酒櫃": 337,b"電熱瓶": 338,b"訊號放大器": 339,b"博視燈": 340,b"顯示器": 341,b"奶瓶蒸鍋": 342,b"放大機": 343,b"電視接受器": 344,b"網路": 345,b"養生壺": 346,b"水床": 347,b"MOD Adpter": 348,b"綠能管理器": 349,b"視訊鏡頭": 350,b"電動玩具": 351,b"綠能主機": 352,b"氣墊床": 353,b"電毯": 354,b"紅酒櫃": 355,b"奶泡機": 356,b"情境燈": 357,b"魚缸 電話": 358,b"保溫電球": 359,b"耳機": 360,b"平板螢幕": 361,b"沉水馬達": 362,b"熱水壺": 363,b"網路電視播放器": 364,b"網路裝置": 365,b"清淨機": 366,b"網路路由器": 367,b"切換器": 368,b"燈 風扇": 369,b"總電源": 370,b"製氧機": 371,b"網路監視器": 372,b"拖地機": 373,b"機板": 374,b"雲端網路": 375,b"電視卡": 376,b"訊號加強器": 377,b"超長波健康床": 378})

	def connOpen(self):
	#happyBase Connection
		
		self.connection = hb.Connection(self.hbServer, autoconnect=False, port=self.hbPort)
		self.connection.open()
		self.table = self.connection.table(self.tableName)
		print("[hb] HBase connection is opening.")

	def connClose(self):
		self.connection.close()
		print("[hb] HBase connection has been closed.")

	def fetchData(self, batchSize, isForTest):
		#print "[hb] Fetching "+str(batchSize)+" app data from HBase..."
		self.x2_ = [] # 宣告二維陣列
		self.tmp2Y = []
		for i in range(int(batchSize)):	# 每次抓取 batchSize 筆資料

			if isForTest == 0:
				self.rowkey = 'row'+str(rd.randint(0, self.maxRow))
			else:
				self.rowkey = 'row'+str(rd.randint(self.testMinRow, self.testMaxRow))

			self.cells = self.table.row(self.rowkey)
			#print( "[hb] > fetch data via key: [" + self.rowkey + "] from HBase.")

			if self.cells[b'content:BUYYEAR'] == 'NA':
				self.x0 = float(-1)
			else:
				self.x0 = float(self.cells[b'content:BUYYEAR'])

			if self.cells[b'content:OLACTIVEPOWER'] == 'NA':
				self.x1 = float(-1)
			else:
				self.x1 = float(self.cells[b'content:OLACTIVEPOWER'])

			if self.cells[b'content:OLAPPARENTPOWER'] == 'NA':
				self.x2 = float(-1)
			else:
				self.x2 = float(self.cells[b'content:OLAPPARENTPOWER'])

			if self.cells[b'content:OLCURRENT'] == 'NA':
				self.x3 = float(-1)
			else:
				self.x3 = float(self.cells[b'content:OLCURRENT'])

			if self.cells[b'content:OLFREQUENCY'] == 'NA':
				self.x4 = float(-1)
			else:
				self.x4 = float(self.cells[b'content:OLFREQUENCY'])

			if self.cells[b'content:OLMAINENERGY'] == 'NA':
				self.x5 = float(-1)
			else:
				self.x5 = float(self.cells[b'content:OLMAINENERGY'])

			if self.cells[b'content:OLPOWERFACTOR'] == 'NA':
				self.x6 = float(-1)
			else:
				self.x6 = float(self.cells[b'content:OLPOWERFACTOR'])

			if self.cells[b'content:OLVOLTAGE'] == 'NA':
				self.x7 = float(-1)
			else:
				self.x7 = float(self.cells[b'content:OLVOLTAGE'])
			
			if self.cells[b'appname:APPNAME'] == 'NA':
				self.x8 = string("UNKNOW")
			else:
				self.x8 = self.cells[b'appname:APPNAME']

			#x_ = [[x0],[x1],[x2],[x3],[x4],[x5],[x6],[x7]]
			self.x_ = [self.x0,self.x1,self.x2,self.x3,self.x4,self.x5,self.x6,self.x7]		# 蒐集第j列資料
			#x2_ = [[x0~x7]
			#		[x0~x7]]
			self.x2_.append(self.x_)						# 附加該列至二維陣列
			#y_ = [0...010...0]
			self.tmpY = [0]*379
			self.tmpY[self.diction[self.x8]] = 1
			self.tmp2Y.append(self.tmpY)
		return self.x2_, self.tmp2Y	

	def fetchData_no_buyYear(self, batchSize, isForTest):
		#print "[hb] Fetching "+str(batchSize)+" app data from HBase..."
		self.x2_ = [] # 宣告二維陣列
		self.tmp2Y = []
		for i in range(int(batchSize)):	# 每次抓取 batchSize 筆資料

			if isForTest == 0:
				self.rowkey = 'row'+str(rd.randint(0, self.maxRow))
			else:
				self.rowkey = 'row'+str(rd.randint(self.testMinRow, self.testMaxRow))
				
			self.cells = self.table.row(self.rowkey)
			#print("[hb]> fetch data via key: [" + self.rowkey + "] from HBase.")

			if self.cells[b'content:OLACTIVEPOWER'] == 'NA':
				self.x1 = float(-1)
			else:
				self.x1 = float(self.cells[b'content:OLACTIVEPOWER'])

			if self.cells[b'content:OLAPPARENTPOWER'] == 'NA':
				self.x2 = float(-1)
			else:
				self.x2 = float(self.cells[b'content:OLAPPARENTPOWER'])

			if self.cells[b'content:OLCURRENT'] == 'NA':
				self.x3 = float(-1)
			else:
				self.x3 = float(self.cells[b'content:OLCURRENT'])

			if self.cells[b'content:OLFREQUENCY'] == 'NA':
				self.x4 = float(-1)
			else:
				self.x4 = float(self.cells[b'content:OLFREQUENCY'])

			if self.cells[b'content:OLMAINENERGY'] == 'NA':
				self.x5 = float(-1)
			else:
				self.x5 = float(self.cells[b'content:OLMAINENERGY'])

			if self.cells[b'content:OLPOWERFACTOR'] == 'NA':
				self.x6 = float(-1)
			else:
				self.x6 = float(self.cells[b'content:OLPOWERFACTOR'])

			if self.cells[b'content:OLVOLTAGE'] == 'NA':
				self.x7 = float(-1)
			else:
				self.x7 = float(self.cells[b'content:OLVOLTAGE'])
			
			if self.cells[b'appname:APPNAME'] == 'NA':
				self.x8 = string("UNKNOW")
			else:
				self.x8 = self.cells[b'appname:APPNAME']

			#x_ = [[x0],[x1],[x2],[x3],[x4],[x5],[x6],[x7]]
			self.x_ = [self.x1,self.x2,self.x3,self.x4,self.x5,self.x6,self.x7]		# 蒐集第j列資料
			#x2_ = [[x0~x7]
			#		[x0~x7]]
			self.x2_.append(self.x_)						# 附加該列至二維陣列
			#y_ = [0...010...0]
			self.tmpY = [0]*379
			self.tmpY[self.diction[self.x8]] = 1
			self.tmp2Y.append(self.tmpY)
		return self.x2_, self.tmp2Y	