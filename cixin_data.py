# -*- coding:gbk -*-
import sys
import re
import os
import time
import datetime
import tushare as ts
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
from internal.common import *

cmp_string = "20150201"
base_date = datetime.datetime.strptime(cmp_string, '%Y%m%d').date()

prepath = "..\\Data\\"
prepath1 = "..\\Data\\entry\\cixin\\"
LOOP_COUNT = 0
df = None
while LOOP_COUNT<3:
	try:
		df = ts.get_stock_basics()
	except:
		LOOP_COUNT += 1
		time.sleep(0.5)
	else:
		break;
if df is None:
	print "Timeout to get stock basic info"
	exit(0)
df1 = df.sort_values(['timeToMarket'], 0, False)

index = -1

wb = Workbook()
# grab the active worksheet
ws = wb.active
strline = u'代码,名称,是否开板,封板天数,封板价格,上市日期,开板日期,开板ZT,流通股本,流通市值,总股本,总市值,封单数量,封单流通比,换手率'
strObj = strline.split(u',')
ws.append(strObj)
#随着列数进行改变
ws.auto_filter.ref = "A1:O1"
excel_row = 2
for code,row in df1.iterrows():
	stockInfo = []
	index += 1
	name = row[0].decode('utf8')
	trade_item = row['timeToMarket']
	liutong_gb = row['outstanding']
	zong_gb = row['totals']
	#print type(trade_item) 竟然是 long 类型
	trade_string = str(trade_item)
	trade_date = datetime.datetime.strptime(trade_string, '%Y%m%d').date()
	delta = trade_date - base_date
	#print (index+1),code,delta.days,trade_date,base_date
	#print (index+1),code,name,trade_date	
	if delta.days<0:
		break

	#获得每只个股每天交易数据
	LOOP_COUNT = 0
	tddf = None
	while LOOP_COUNT<3:
		try:
			tddf = ts.get_k_data(code)
		except:
			LOOP_COUNT += 1
			time.sleep(0.5)
		else:
			break;
	if tddf is None:
		print "Timeout to get k data of " + code +", Quit"
		exit(0)

	b_open = 0
	yzzt_day = 0
	last_close = 0.0
	td_total = len(tddf)
	fengban_vol = 0		#封板数量
	fengliu_prop = 0.0
	last_day_vol = 0.0
	turnover = 0.0
	open_date = 0
	kbzt_days = 0
	for tdidx,tdrow in tddf.iterrows():
		open = tdrow[1]
		close = tdrow[2]
		high = tdrow['high']
		low = tdrow['low']
		last_day_vol = tdrow['volume']
		#high == low 意味YZZT
		if high==low:
			yzzt_day += 1
			last_close = close
			if b_open==1:
				kbzt_days += 1
			continue

		#新股第一天可能 high!=low
		if yzzt_day!=0:
			b_open = 1
			opn_date_str = tdrow['date']
			#近似涨停处理
			zt_price = last_close * 1.0992
			#print code,name,last_close,close,zt_price
			if close>=zt_price or high>=zt_price:
				kbzt_days += 1
			else:
				break
		else:
			#针对特殊新股：招商蛇口、温氏股份等
			if open<=close and close==high and low==open:
				yzzt_day += 1
			else:
				b_open = 1
				opn_date_str = tdrow['date']
				break
		last_close = close

	if b_open==0:
		LOOP_COUNT = 0
		trdf = None
		while LOOP_COUNT<3:
			try:
				trdf = ts.get_realtime_quotes(code)
			except:
				LOOP_COUNT += 1
				time.sleep(0.5)
			else:
				break;
		if trdf is None:
			print "Timeout to get real time quotes"
			exit(0)

		volstr = trdf.iloc[0,10]
		if volstr.isdigit() is True:
			fengban_vol = int(volstr)
			fengliu_prop = fengban_vol/(liutong_gb*10000)
			turnover = last_day_vol/(liutong_gb*10000)
	elif b_open==1:
		opn_date_int = ''.join(opn_date_str.split('-'))
		open_date = int(opn_date_int)

	#追加数据,流通市值、总市值
	liutong_sz = liutong_gb*last_close
	zong_sz = zong_gb*last_close
	stockInfo.append(code)
	stockInfo.append(name)
	stockInfo.append(b_open)
	stockInfo.append(yzzt_day)
	stockInfo.append(last_close)
	stockInfo.append(trade_item)
	stockInfo.append(open_date)
	stockInfo.append(kbzt_days)
	stockInfo.append(liutong_gb)
	stockInfo.append(round(liutong_sz,2))
	stockInfo.append(zong_gb)
	stockInfo.append(round(zong_sz,2))
	stockInfo.append(fengban_vol)
	stockInfo.append(round(fengliu_prop,2))
	stockInfo.append(round(turnover,2))
	#print stockInfo

	k = 0
	ascid = 65
	number = len(stockInfo)
	for k in range(0,number):
		cell = chr(ascid+k) + str(excel_row)
		ws[cell] = stockInfo[k]
	excel_row += 1

filexlsx = prepath + "cixin_analyze.xlsx"
wb.save(filexlsx)

today = datetime.date.today()
cur=datetime.datetime.now()
qdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
filexlsx1 = prepath1 + "cx_anly_"+ qdate
filexlsx1 = '%s_%02d-%02d.xlsx' %(filexlsx1, cur.hour, cur.minute)
wb.save(filexlsx1)

