#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
import shutil

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

#�����ļ�
filetxt = "a.txt"
file2 = "file2.txt"
shutil.copy(filetxt, file2)
