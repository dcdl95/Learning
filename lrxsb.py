import pandas as pd
import numpy as np

# 读取原始数据
file_path = '/Users/licheng/Desktop/work/项目资料/浙江森日/负荷数据 - 2024-07-08T162010.117-06.xlsx'  # 替换为你的数据文件路径
df = pd.read_excel(file_path)

# 数据清理与处理
# 保留指定列
columns_to_keep = ['日期', '瞬时功率', '正向有功', 'CT', 'PT']
df = df[columns_to_keep]

# 日期列分离为日期和时间
df[['日期', '时间']] = df['日期'].str.split(' ', 1, expand=True)

# 确保瞬时功率和正向有功为数字格式
df['瞬时功率'] = pd.to_numeric(df['瞬时功率'], errors='coerce')
df['正向有功'] = pd.to_numeric(df['正向有功'], errors='coerce')

# 计算变比（如果需要）
df['瞬时功率'] = df['瞬时功率'] * df['CT'] * df['PT']
df['正向有功'] = df['正向有功'] * df['CT'] * df['PT']

# 排序日期和时间
df = df.sort_values(by=['日期', '时间'])

# 构建辅助列
# 假设时间列为小时数，并构建指定时段的辅助列
time_slots = [0, 8, 9, 11, 13, 15, 17, 23]
for slot in time_slots:
    df[f'辅助列_{slot}'] = df['时间'].apply(lambda x: 1 if int(x.split(':')[0]) == slot else 0).cumsum()

# 计算各时段最大值
max_values = {}
for slot in time_slots:
    max_values[slot] = df[f'辅助列_{slot}'].max()

# 建立新列，对应行数填充
new_df = pd.DataFrame()
new_df['日期'] = df['日期'].unique()
for slot in time_slots:
    new_df[f'{slot}点行数'] = [df[(df['日期'] == date) & (df[f'辅助列_{slot}'] == max_values[slot])].index[0] for date in new_df['日期']]

# 保存处理后的数据
output_file = '/Users/licheng/Desktop/work/项目资料/浙江森日/processed_data1.xlsx'
with pd.ExcelWriter(output_file) as writer:
    df.to_excel(writer, sheet_name='原始数据处理后')
    new_df.to_excel(writer, sheet_name='辅助列对应行数')

print(f'数据处理完成，结果保存在 {output_file} 文件中')
