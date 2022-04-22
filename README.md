# 以深度學習為基礎進行霧季預測分析-以金門為例
## 資料處理
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
