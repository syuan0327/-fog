import re
import bs4,requests
import csv,time


url='https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=467110&stname=%25E9%2587%2591%25E9%2596%2580&datepicker='+'2022-04-18'+'&altitude=47.9m'
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
    table.append(['2022/04/19',a[0],a[3],a[4],a[5],a[7]])
    start+=17
    m+=1
    

print(table)