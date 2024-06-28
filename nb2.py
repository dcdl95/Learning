import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def process_data(file_path, summary_path, plot_path, power_usage_path):
    # 读取CSV文件，指定时间列为索引列
    data = pd.read_csv(file_path, parse_dates=['time'], index_col='time')

    # 定义时间段
    time_ranges = {
        '00:00-08:00': ('00:00', '08:00'),
        '09:00-11:00': ('09:00', '11:00'),
        '11:00-13:00': ('11:00', '13:00'),
        '13:00-15:00': ('13:00', '15:00'),
        '15:00-17:00': ('15:00', '17:00'),
        '17:00-23:00': ('17:00', '23:00'),
    }

    # 准备功率使用结果
    power_usage_results = []

    # 处理每个时间段
    for label, (start, end) in time_ranges.items():
        mask = (data.index.time >= pd.to_datetime(start).time()) & (data.index.time < pd.to_datetime(end).time())
        filtered_power = data.loc[mask, 'data2']
        # 计算功率计量差值（用电量）
        power_usage = filtered_power.resample('D').apply(lambda x: x.iloc[-1] - x.iloc[0] if len(x) > 0 else 0)  # 结束值减去起始值
        power_usage_stats = power_usage.agg(['mean', 'max', 'min'])
        power_usage_results.append(power_usage_stats.rename(label))

    # 保存功率使用统计数据
    power_usage_df = pd.DataFrame(power_usage_results).T  # 转置以便每个时间段为一列
    power_usage_df.to_csv(power_usage_path)

    # 绘制图像
    plt.figure(figsize=(12, 8))
    for date, group in data.groupby(data.index.date):
        times = group.index.map(lambda dt: pd.Timestamp(year=2024, month=1, day=1, hour=dt.hour, minute=dt.minute, second=dt.second))
        plt.plot(times, group['data'], label=str(date))

    # 添加每个时间段的平均值、最大值和最小值的水平线
    for label, stats in zip(time_ranges.keys(), power_usage_results):
        start_time, end_time = time_ranges[label]
        plt.hlines(stats['mean'], pd.to_datetime('2024-01-01 ' + start_time), pd.to_datetime('2024-01-01 ' + end_time), colors='green', linestyles='--', label=f'Mean {label}')
        plt.hlines(stats['max'], pd.to_datetime('2024-01-01 ' + start_time), pd.to_datetime('2024-01-01 ' + end_time), colors='red', linestyles=':', label=f'Max {label}')
        plt.hlines(stats['min'], pd.to_datetime('2024-01-01 ' + start_time), pd.to_datetime('2024-01-01 ' + end_time), colors='blue', linestyles='-.', label=f'Min {label}')

    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gcf().autofmt_xdate()
    plt.title('Daily Data Variation with Statistical Annotations')
    plt.xlabel('Time of Day')
    plt.ylabel('Data')
    plt.grid(True)
    plt.legend(title='Date and Stats', loc='upper left', bbox_to_anchor=(1.05, 1))  # 将图例放到图外
    plt.tight_layout()  # 调整整体布局以适应图例
    plt.savefig(plot_path)
    plt.show()

# 使用示例
file_path = '/Users/licheng/Desktop/work/宏伟食品/output.csv'
summary_path = '/Users/licheng/Desktop/work/宏伟食品/5_1.csv'
plot_path = '/Users/licheng/Desktop/work/宏伟食品/5.png'
power_usage_path = '/Users/licheng/Desktop/work/宏伟食品/5_2.csv'
process_data(file_path, summary_path, plot_path, power_usage_path)
