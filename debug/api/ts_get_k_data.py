#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import datetime
import tushare as ts

'''
    ��ȡk������
    ---------
    Parameters:
      code:string
                  ��Ʊ���� e.g. 600848
      start:string
                  ��ʼ���� format��YYYY-MM-DD Ϊ��ʱȡ��������
      end:string
                  �������� format��YYYY-MM-DD Ϊ��ʱȡ���һ��������
      ktype��string
                  �������ͣ�D=��k�� W=�� M=�� 5=5���� 15=15���� 30=30���� 60=60���ӣ�Ĭ��ΪD
      autype:string
                  ��Ȩ���ͣ�qfq-ǰ��Ȩ hfq-��Ȩ None-����Ȩ��Ĭ��Ϊqfq
      index:bool
                  True or False �Ƿ���ָ��
      retry_count : int, Ĭ�� 3
                 ��������������ظ�ִ�еĴ��� 
      pause : int, Ĭ�� 0
                �ظ��������ݹ�������ͣ����������ֹ������ʱ��̫�̳��ֵ�����
    return
    -------
      DataFrame
          date �������� (index)
          open ���̼�
          high  ��߼�
          close ���̼�
          low ��ͼ�
          volume �ɽ���
          amount �ɽ���
          turnoverratio ������
          code ��Ʊ����
'''
	
pindex = len(sys.argv)
code='300611'
if pindex==2:
	code = sys.argv[1]

LOOP_COUNT=0
while LOOP_COUNT<3:
	try:
		df = ts.get_k_data(code)
	except:
		LOOP_COUNT += 1
		time.sleep(0.5)
	else:
		break;
if df is None:
	print "Timeout to get hist data"
	exit(0)

print df.head(10)

df1 = df.sort_index(ascending=False)
print "\nReverse:"
print df1.head(10)
