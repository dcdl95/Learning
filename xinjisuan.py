import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import os

# 设置Matplotlib支持中文显示
matplotlib.rcParams['font.family'] = 'Arial Unicode MS'
matplotlib.rcParams['axes.unicode_minus'] = False

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
output_folder = '/Users/licheng/Desktop/work/宏伟食品/630_999'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 准备存储结果
results = []

# 对每个时间段进行处理和绘图
for start, end in time_periods:
    plt.figure(figsize=(12, 8))
    time_range = pd.date_range(start='2000-01-01 ' + start, end='2000-01-01 ' + end, freq='T').time
    all_powers = []

    # 绘制每一天该时间段内的功率数据
    for date, day_data in data.groupby(data.index.date):
        period_data = day_data.between_time(start, end)
        plt.plot(time_range, period_data['power'], label=f'{date} 实际功率')
        all_powers.append(period_data['power'])

    # 如果有数据，计算并绘制最大值、最小值和平均值线
    if all_powers:
        combined_powers = pd.concat(all_powers, axis=1)
        max_power = combined_powers.max(axis=1)
        min_power = combined_powers.min(axis=1)
        mean_power = combined_powers.mean(axis=1)

        plt.plot(time_range, max_power, 'r--', label='最大功率')
        plt.plot(time_range, min_power, 'g--', label='最小功率')
        plt.plot(time_range, mean_power, 'b--', label='平均功率')

        # 保存统计结果到CSV数据
        daily_result = {
            'time_period': f'{start}-{end}',
            'max_power': max_power.mean(),
            'min_power': min_power.mean(),
            'mean_power': mean_power.mean()
        }
        results.append(daily_result)

    plt.title(f'功率曲线 {start}-{end}')
    plt.xlabel('时间')
    plt.ylabel('功率 (kW)')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, f'{start}-{end}.png'))
    plt.close()

# 将结果转换为DataFrame并保存到CSV文件
results_df = pd.DataFrame(results)
results_df.to_csv('/Users/licheng/Desktop/work/宏伟食品/630_9.csv', index=False)

print("分析完成，结果已保存到 output_data.csv，相关图形已保存到文件夹 " + output_folder)
