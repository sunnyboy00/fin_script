#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import tushare as ts

yzzt_list = ['603345','603238','000520','300613','300608','300553','603615']
excecount = 0
stdf = None
while excecount<5:
	try:
		stdf = ts.get_realtime_quotes(yzzt_list)
	except:
		print "Get except:"
		time.sleep(0.5)
		excecount += 1
		stdf = None
	else:
		break
if stdf is None:
	print "Get list fail at:", yzzt_list
	exit(0)
	
s=[]
for index,row in stdf.iterrows():
	stockInfo = []
	code = yzzt_list[index]
	index += 1
	name = row[0]
	print type(name)
	s.append(name)
	print code,name

print s
print u'[' + u','.join(u"'""'" + unicode(x) + u"'" for x in s) + u']'

#���������ӡ����Ҫ�ȶ������������
reload(sys)
sys.setdefaultencoding('gbk')
print '[' + ','.join("'""'" + str(x) + "'" for x in s) + ']'
