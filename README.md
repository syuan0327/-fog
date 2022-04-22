# 以深度學習為基礎進行霧季預測分析-以金門為例
## 資料處理
### 原資料來源
1. 金門氣象站
2. [觀測資料查詢系統](https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp?fbclid=IwAR3xkKHGTOGAcEZqRmySsKIu5RkF8IRuzUJb-j_PYUuzM2oTdcsusQGDpqU)
3. [天氣與氣候監測網](https://watch.ncdr.nat.gov.tw/watch_vis)
### 原資料處理
由於金門氣象站給予的資料只有能見度及日期，所以使用了爬蟲的方式，上網爬取了能作為訓練資料的的天氣因子，並將能見度750m作為是否起霧的基準加上Label，且由於原資料並無全部完整，因此這邊先將不完整處設為無能見度，稍後下面會在示範如何處理。完整程式如下。


```python
import re
import bs4,requests
import csv,time


dates=[]
hours=[]
see=[]
date=[]
sees=[]
from collections import Counter   #引入Counter


with open('a.csv', newline='',encoding='utf-8') as csvfile:

  # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)

  
    for row in rows:
        dates.append(row[0])
        hours.append(row[1])
        see.append(row[2])
    b = dict(Counter(dates))
    for key,value in b.items():
        if value >= 1:
            #整理過的date
            date.append(key)
    for i in range(0,len(see),24):
        sees.append(see[i:i+24])


print(sees)



for i in range(len(date)):
    url='https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=467110&stname=%25E9%2587%2591%25E9%2596%2580&datepicker='+date[i]+'&altitude=47.9m'
    print(url)
    htmlFile=requests.get(url)
        
    objSoup= bs4.BeautifulSoup(htmlFile.text,'html.parser') #解析網站
    txt=objSoup.text.split() #以split分隔讀取到的網頁內容並存成list  
    start=60
    m=0
    table=[]
    while m < 24:
        a=[]
        for j in range(start,start+8): #j為讀取標題，時間、溫度等24筆
            a.append(txt[j])  
        table.append([date[i],a[0],a[3],a[4],a[5],a[7],sees[i][m]])
        start+=17
        m+=1
    
    for i in range(len(table)):
        if table[i][6] == '' or table[i][6]=='/':
            table[i].append('No visibility')
        else:
            if float(table[i][6])>0.75:
                table[i].append('1')
            elif float(table[i][6])<=0.75:
                table[i].append('0')

    with open('0419-2.csv','a',newline='')as csvfile:
        writer = csv.writer(csvfile)

        # 寫入二維表格
        writer.writerows(table)
    
```
#### 原資料

![image](https://user-images.githubusercontent.com/47874861/164650229-8b9a9670-030b-4620-9b7d-83922803a18f.png)

#### 處理後

![image](https://user-images.githubusercontent.com/47874861/164650370-8af70138-6c85-4f13-95af-17e42fecdcb6.png)


### 補齊缺失的資料

接著要處理缺失的資料，所以去爬取了天氣與氣候監測網的金門能見度相互比對後再進行更新資料的動作

visibility.py
```python
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
```
#### 資料處理
由於是否起霧的資料比相差太大，因此使用了以下兩種方式來進行資料處理，程式如下：

1.  oversampling
2.  undersampling

undersampling
```ptyhon
from cv2 import threshold
import pandas as pd
from collections import Counter
from imblearn.over_sampling import RandomOverSampler, SMOTE  
from imblearn.under_sampling import RandomUnderSampler 
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')
print(data.info())


X = data.drop(columns='Label')
y = data['Label']

rus = RandomUnderSampler(random_state=0)
X_undersampled, y_undersampled = rus.fit_resample(X,y) 
df = pd.merge(X_undersampled, y_undersampled,left_index=True,right_index=True)
df.to_csv('undersampler.csv')

plt.figure( figsize=(10,5) )
data['Label'].value_counts().plot( kind='pie', colors=['lightcoral','skyblue'], autopct='%1.2f%%' )
plt.title( 'Label' )  
plt.ylabel( '' )
plt.show()
```
oversampling
```ptyhon
from cv2 import threshold
import pandas as pd
from collections import Counter
from imblearn.over_sampling import RandomOverSampler, SMOTE  
from imblearn.under_sampling import RandomUnderSampler 
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')
print(data.info())


X = data.drop(columns='Label')
y = data['Label']

ros = RandomOverSampler(random_state=0)  
X_oversampled, y_oversampled = ros.fit_resample(X, y) 
df = pd.merge(X_oversampled, y_oversampled,left_index=True,right_index=True)


plt.figure( figsize=(10,5) )
df['Label'].value_counts().plot( kind='pie', colors=['lightcoral','skyblue'], autopct='%1.2f%%' )
plt.title( 'Label' ) 
plt.ylabel( '' )
plt.show()
```


