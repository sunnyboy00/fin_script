#!/usr/bin/env python
# -*- coding:gbk -*-
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import sys
import re
import os
import time
import datetime

from internal.common import *

prepath = "../Data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"

#向第一页发起HTTP Get请求，获得所有Web数据并写入文件
pindex = len(sys.argv)
if pindex<3:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 时间<YYYY-MM-DD or MM-DD> [arr=[number, number...]]\n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

head3 = code[0:3]
result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
if result is True:
	code = "sz" + code
else:
	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
	if result is True:
		code = "sh" + code
	else:
		print "非法代码:" +code+ "\n"
		exit(1);
#print code

today = datetime.date.today()
ret,stdate = parseDate(sys.argv[2], today)
if ret==-1:
	exit(1)

qarr = ''
if pindex==4:
	qarr = sys.argv[3]

edate = datetime.datetime.strptime(stdate, '%Y-%m-%d').date()
delta = edate - today
if (delta.days>=0):
	print "Warning:日期可能不正确，导致数据错误！"

url = url +"?date="+ stdate +"&symbol="+ code
urlall = url + "&page=1"

excecount = 0
while True:
	if excecount>10:
		break;

	#创建url链接，获取每一页的数据
	try:
		req = urllib2.Request(urlall)
		res_data = urllib2.urlopen(req, timeout=3).readlines()
		lineCount = len(res_data)
	except:
		print "Get URL except"
		excecount += 1
		continue
	else:
		file = prepath + "st_data.txt"
		fcsv = open(file, 'w')

		idx = 0
		while True:
			if idx>=lineCount:
				break
			line = res_data[idx]
			idx += 1
			fcsv.write(line)

		fcsv.close()
		break;


