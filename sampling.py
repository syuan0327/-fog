from cv2 import threshold
import pandas as pd
from collections import Counter
from imblearn.over_sampling import RandomOverSampler, SMOTE  # 随机采样函数 和SMOTE过采样函数
from imblearn.under_sampling import RandomUnderSampler 
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')
print(data.info())

# 分别获取特征值和标签值
X = data.drop(columns='Label')
y = data['Label']

plt.figure( figsize=(10,5) )
data['Label'].value_counts().plot( kind='pie', colors=['lightcoral','skyblue'], autopct='%1.2f%%' )
plt.title( 'Label' )  # 圖標題
plt.ylabel( '' )
plt.show()
'''
# 对标签中的变量进行计数统计
print('原始标签数据统计：', Counter(y))
rus = RandomUnderSampler(random_state=0)
X_undersampled, y_undersampled = rus.fit_resample(X,y) 
df = pd.merge(X_undersampled, y_undersampled,left_index=True,right_index=True)
df.to_csv('undersampler.csv')


'''
# 随机过采样方法
ros = RandomOverSampler(random_state=0)  # random_state为0（此数字没有特殊含义，可以换成其他数字）使得每次代码运行的结果保持一致
X_oversampled, y_oversampled = ros.fit_resample(X, y)  # 使用原始数据的特征变量和目标变量生成过采样数据集
df = pd.merge(X_oversampled, y_oversampled,left_index=True,right_index=True)


plt.figure( figsize=(10,5) )
df['Label'].value_counts().plot( kind='pie', colors=['lightcoral','skyblue'], autopct='%1.2f%%' )
plt.title( 'Label' )  # 圖標題
plt.ylabel( '' )
plt.show()