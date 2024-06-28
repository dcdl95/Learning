import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

# 设置Matplotlib支持中文显示
matplotlib.rcParams['font.family'] = 'Arial Unicode MS'  # 设置字体为Arial Unicode MS
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 加载CSV文件
data = pd.read_csv('/Users/licheng/Desktop/work/宏伟食品/630.csv', names=['date', 'power', 'meter_reading'], header=0)
data['date'] = pd.to_datetime(data['date'])

# 将日期时间设置为索引
data.set_index('date', inplace=True)

# 定义时间段
time_periods = [
    ('00:00', '08:00'), ('08:00', '09:00'), ('09:00', '11:00'), ('11:00', '13:00'),
    ('13:00', '15:00'), ('15:00', '17:00'), ('17:00', '23:00'), ('23:00', '00:00')
]

# 创建文件夹保存图片
output_folder = '/Users/licheng/Desktop/work/宏伟食品/630___1111'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 准备存储结果
results = []

# 对每一天的数据进行处理
for date, day_data in data.groupby(data.index.date):
    daily_result = {'date': date}
    for start, end in time_periods:
        # 筛选特定时间段的数据
        period_data = day_data.between_time(start, end)
        if not period_data.empty:
            max_power = period_data['power'].max()
            min_power = period_data['power'].min()
            mean_power = period_data['power'].mean()
            start_meter = period_data['meter_reading'].iloc[0]
            end_meter = period_data['meter_reading'].iloc[-1]
            energy_consumption = end_meter - start_meter

            daily_result[f'{start}-{end} max power'] = max_power
            daily_result[f'{start}-{end} min power'] = min_power
            daily_result[f'{start}-{end} mean power'] = mean_power
            daily_result[f'{start}-{end} energy consumption'] = energy_consumption
        else:
            daily_result[f'{start}-{end} max power'] = float('nan')
            daily_result[f'{start}-{end} min power'] = float('nan')
            daily_result[f'{start}-{end} mean power'] = float('nan')
            daily_result[f'{start}-{end} energy consumption'] = float('nan')

    results.append(daily_result)

# 将结果转换为DataFrame并保存到CSV文件
results_df = pd.DataFrame(results)
results_df.to_csv('/Users/licheng/Desktop/work/宏伟食品/630_333.csv', index=False)

# 绘制图形
for period in time_periods:
    plt.figure(figsize=(12, 8))
    all_data = pd.concat([day_data.between_time(*period)['power'] for date, day_data in data.groupby(data.index.date) if not day_data.between_time(*period).empty], axis=1)

    all_data.plot(ax=plt.gca(), legend=None, alpha=0.5)  # Plot all days' data
    plt.axhline(y=all_data.max().max(), color='r', linestyle='--', label='最大功率')
    plt.axhline(y=all_data.min().min(), color='g', linestyle='--', label='最小功率')
    plt.axhline(y=all_data.mean().mean(), color='b', linestyle='--', label='平均功率')

    start, end = period
    plt.title(f'功率曲线 {start}-{end}')
    plt.xlabel('时间')
    plt.ylabel('功率 (kW)')
    plt.legend()
    plt.savefig(os.path.join(output_folder, f'{start}-{end}.png'))
    plt.close()

print("分析完成，结果已保存到 output_data.csv，相关图形已保存到文件夹 " + output_folder)
