import pandas as pd
from fitparse import FitFile

# 加载.fit文件
fit_file = FitFile('/Users/licheng/Desktop/MATCH_875600-2024-08-26-05-28-46-log.st.fit')

# 创建一个列表来保存数据
data = []

# 遍历.fit文件中的所有消息
for record in fit_file.get_messages('record'):
    record_data = {}
    for data_field in record:
        record_data[data_field.name] = data_field.value
    data.append(record_data)

# 将列表转换为DataFrame
df = pd.DataFrame(data)

# 将DataFrame保存为.csv文件
csv_file_path = '/Users/licheng/Desktop/MATCH_875600-2024-08-26-05-28-46-log.st.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8')

print(f"CSV文件已保存到 {csv_file_path}")

