#氣象站資料整理
import csv
import numpy as np
date=[]
data=[]
pop_num=[]
a=0
# 開啟 CSV 檔案
with open('origin20202022.csv', newline='') as csvfile:

  # 讀取 CSV 檔案內容
  rows = csv.reader(csvfile)

  # 以迴圈輸出每一列
  for row in rows:
      date.append(row[0])
      data.append(row[1])
'''
for i in range(len(data)):
    if data[i]=='' or data[i]=='/':
        pop_num.append(i)
for i in range(len(pop_num)-1,-1,-1):
    data.pop(pop_num[i])
    date.pop(pop_num[i])'''
table=[]
for i in range(len(data)):
    table.append((date[i]+' '+data[i]).split(' '))
with open('a.csv', 'a',newline='') as csvfile:
  writer = csv.writer(csvfile)

  # 寫入二維表格
  writer.writerows(table)