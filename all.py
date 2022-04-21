import pandas as pd

data = pd.read_csv('0419-2.csv')
print(data.info())

# 分别获取特征值和标签值
X = data.drop(columns='visibility')

X.to_csv('0419-3.csv',index=False)