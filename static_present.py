# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import tushare as ts
from internal.ts_common import *

curdate = ''
data_path = "..\\Data\\_self_define.txt"
stockCode = []

today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate

#˵��show_flag
#0�������ÿһֻ����ͨ�̣�������㻻����
#1�����ÿһֻ����ͨ�̣����Ҽ��㻻����
#2����ʾÿһֻ���µ����ţ����������ȫ����ʾ������û��ֻ��ʾһ��news
pindex = len(sys.argv)

st_bas=ts.get_stock_basics()
st_bas.to_excel("a_stock_base.xlsx")
st_pb_base = st_bas[st_bas.pb!=0]
st_pb_base = st_pb_base.sort_values(['timeToMarket'], 0, False)
st_pb_base.to_excel("a_stock_pb_base.xlsx")
st_index = st_pb_base.index
st_list=list(st_index)

number = len(st_list)
if number<=0:
	exit(0)

b_get_data = 1
#ZTһ��ȡ�� base ��
#��ȡlist��ͨ��������ʼλ��
base = 23
loop_ct = number/base
if number%base!=0:
	loop_ct += 1
for i in range(0, loop_ct):
	end_idx = min(base*(i+1), number)
	cur_list = st_list[i*base:end_idx]
	if len(cur_list)==0:
		break
	#print cur_list
	stdf = ts.get_realtime_quotes(cur_list)

	#print stdf
	for index,row in stdf.iterrows():
		stockInfo = []
		code = cur_list[index]
		index += 1
		name = row[0]
		#ltgb = row['outstanding']
		#zgb = row['totals']

		high = row['high']
		low = row['low']
		open = row['open']
		price = row['price']
		pre_close = row['pre_close']
		print index, code,name,open,low,high,price,pre_close

		#ͨ�����K�����ݣ��ж��Ƿ�YZZT�¹�
		if b_get_data == 1:
			#���ÿֻ����ÿ�콻������
			day_info_df = ts.get_k_data(code)
			#print day_info_df
			trade_days = len(day_info_df)

			#��ΪYZZT���ᳬ�� 32 ��������
			if trade_days>32:
				b_get_data = 0
		yz_type = check_yzzt(code, name, row)
	if i>2:
		break

