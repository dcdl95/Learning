import pandas as pd

# 读取CSV文件的前几行数据
file_path = '/Users/licheng/Desktop/66a792d601a97d024a7ec820.csv'
df = pd.read_csv(file_path, encoding='utf-8')
print(df.head())
