import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def process_data(file_path, summary_path, plot_path):
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

    # 准备统计结果和直线标注数据
    summary_results = []
    lines_data = []

    # 处理每个时间段
    for label, (start, end) in time_ranges.items():
        mask = (data.index.time >= pd.to_datetime(start).time()) & (data.index.time < pd.to_datetime(end).time())
        filtered_data = data[mask]
        stats = filtered_data.resample('D').agg(['mean', 'max', 'min']).rename(
            columns={'data': 'Data', 'mean': 'Mean', 'max': 'Max', 'min': 'Min'})
        stats.columns = stats.columns.droplevel(0)
        stats['Time Range'] = label
        summary_results.append(stats)

        # 计算全时间段内的统计值
        overall_stats = filtered_data['data'].agg(['mean', 'max', 'min'])
        lines_data.append(
            (overall_stats, pd.to_datetime('2024-01-01 ' + start), pd.to_datetime('2024-01-01 ' + end), label))

    # 合并所有统计结果
    summary_df = pd.concat(summary_results)
    summary_df.to_csv(summary_path)

    # 绘制图像
    plt.figure(figsize=(12, 8))
    for date, group in data.groupby(data.index.date):
        times = group.index.map(
            lambda dt: pd.Timestamp(year=2024, month=1, day=1, hour=dt.hour, minute=dt.minute, second=dt.second))
        plt.plot(times, group['data'], label=str(date))

    # 添加每个时间段的平均值、最大值和最小值的水平线
    for stats, start_time, end_time, label in lines_data:
        plt.hlines(stats['mean'], start_time, end_time, colors='green', linestyles='--', label=f'Mean {label}')
        plt.hlines(stats['max'], start_time, end_time, colors='red', linestyles=':', label=f'Max {label}')
        plt.hlines(stats['min'], start_time, end_time, colors='blue', linestyles='-.', label=f'Min {label}')

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
file_path = '/Users/licheng/Desktop/work/宏伟食品/宏伟食品测试/宏伟食品测试（4.26-5.8）/630kVA/630.csv'
summary_path = '/Users/licheng/Desktop/work/宏伟食品/宏伟食品测试/宏伟食品测试（4.26-5.8）/630kVA/630_1.csv'
plot_path = '/Users/licheng/Desktop/work/宏伟食品/宏伟食品测试/宏伟食品测试（4.26-5.8）/630kVA/630.png'
process_data(file_path, summary_path, plot_path)
