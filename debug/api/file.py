# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook

#����Ŀ¼�µ�������Ŀ¼���ļ�
path = "."
for (dirpath, dirnames, filenames) in os.walk(path):
	print len(filenames)
	file_list = filenames

#�����г�Ŀ¼�µ���Ŀ¼���ļ�
for f in os.listdir(path):
	print f

#�ж����ļ�����Ŀ¼
if(os.path.isdir(path + '/' + f)):
	pass
if(os.path.isfile(path + '/' + f)):
	pass

