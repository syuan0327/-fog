#機場能見度
from ast import If
from bs4 import BeautifulSoup
from cv2 import split
from matplotlib.pyplot import draw_if_interactive
from numpy import c_
import requests,time
import re
import bs4,requests
import csv
import datetime as dt
startdate = dt.datetime(2020, 7,31)
enddate = dt.datetime(2020, 8,30)
data=[]
datas=[]
totaldays = (enddate - startdate).days + 1

    #在for迴圈內作業。  
for daynumber in range(totaldays):
    datestring = (startdate + dt.timedelta(days = daynumber)).date()
    for hour in range(25):
        url='https://watch.ncdr.nat.gov.tw/php/list_vis_obs_csv.php?d='+str(datestring)+'&t='+str(hour)+':00'
        news1=requests.get(url)
        soup1=BeautifulSoup(news1.text,'html.parser')
        a=soup1.prettify().split('\n')
        data.append(a)
del_num=[]
for i in range(len(data)-1):
    for j in data[i]:
        datas.append(j.split(','))
for i in range(len(datas)-1):
    if datas[i]==['']:
        del_num.append(i)
for i in range(len(del_num)-1,-1,-1):
    datas.pop(del_num[i])
table=[]
for i in range(len(datas)-1):
    if (datas[i][1]=='金門機場') :
        a=int(datas[i][3])/1000
        table.append((datas[i][4]+' '+str(a)).split(' '))
print(table)
with open('test'+'.csv', 'a',newline='') as csvfile:
  writer = csv.writer(csvfile)

  # 寫入二維表格
  writer.writerows(table)

   
'''
    for i in range(len(a)):
        data.append(a[i].split(','))
        for i in range(len(data)-2):
            if data[i][1]=='金門機場'or data[i][1]=='金門水頭'or data[i][1]=='金門料羅' :
                print(data[i][1],data[i][3],data[i][4])'''