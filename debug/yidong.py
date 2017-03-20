# -*- coding:gbk -*-
from bs4 import BeautifulSoup as BS
import urllib.request as ur
import os
import sqlite3
import pandas as pd
# conn = sqlite3.connect('d:/stock/mainforce.db')
# sql = 'insert into lhb(code,day,typ,ranking,depart,buy,buyrate,sell,sellrate,net_value) VALUES (?,?,?,?,?,?,?,?,?,?)'
# cur =conn.cursor()
'''����������������࣬���ϼƵ�����'''
url = 'http://data.eastmoney.com/stock/lhb.html'
urlread = ur.urlopen(url)
html = urlread.read().decode('gbk','ignore')
soup = BS(html,'lxml')
table = soup.select('table')
htmlist = []
td = table[0].select('td')              # �Ϻ�������
for i in range(1,len(td)):
    first ="http://data.eastmoney.com/stock"+str(td[i])[33:55]
    htmlist.append(first)
td1 = table[1].select('td')
for r in range(1,len(td1)):
    first1 ="http://data.eastmoney.com/stock"+str(td1[r])[33:55]
    htmlist.append(first1)
x = []
for lhburl in htmlist:
    # print(lhburl)
    try:
        lhburlread = ur.urlopen(lhburl)
        lhbhtml = lhburlread.read().decode('gbk', 'ignore')
    except:
        fl = open('d: st.txt', 'a')            # �����ɹ���ҳ������
        fl.write(code)
        fl.write("\n")
        fl.close()
    else:
        lhbsoup = BS(lhbhtml, 'lxml')
        list = lhbsoup.find_all('div', attrs={'class':'content-sepe'})      # �м����ϰ����� ����
        list1 = lhbsoup.find_all('div', attrs={'class':'left con-br'})        # ȡ���� ����
        code = lhburl[42:48]            # ��Ʊ����
        print(code)
        for i in range(len(list)):
            day = list1[i].text[:10]       #�ϰ�����
            l = list1[i].text.index('��')         # l�ַ�ֵ��Ϊ�ϰ�����
            typ = list1[i].text[(l+1):]        # �ϰ�����
            lhbtab = list[i].select('table')       #��ȡ��ֵ
            for r in range(len(lhbtab)):
                lhbtr = lhbtab[r].select('tr')
                for d in range(2,len(lhbtr)):
                    lhbtd = lhbtr[d].select('td')
                    if len(lhbtd) == 7:
                        ranking =(lhbtd[0].text)                  #����
                        depart =(lhbtd[1].select('a')[1].text)        #Ӫҵ��
                        buy =(lhbtd[2].text)                   #��������Ԫ
                        buyrate = (lhbtd[3].text)                  #����ռ��
                        sell =(lhbtd[4].text)                # ����
                        sellrate =(lhbtd[5].text)                # ����ռ��
                        net_value=(lhbtd[6].text)                 # �ϼ�����
                        y=(code,day,typ,ranking,depart,buy,buyrate,sell,sellrate,net_value)
                        # cur.execute(sql,y)
                        # print(y)
                        x.append(y)
# conn.commit()
# cur.close()
# conn.close()
df = pd.DataFrame(x, columns=['��Ʊ����','�ϰ�����','�ϰ�ԭ��','����','Ӫҵ��','�����','����ռ��','������','����ռ��','��ֵ'])
print(df)
