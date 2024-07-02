import xlrd
import csv
import os


def extract_data_from_xls(directory):
    data_to_write = []
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".xls"):
            path = os.path.join(directory, filename)
            workbook = xlrd.open_workbook(path)
            sheet = workbook.sheet_by_index(0)  # 假设数据在第一个sheet中
            # 确保不超过实际的行数
            nrows = sheet.nrows
            for row_index in range(2, min(nrows, 98)):  # 取实际行数和98中较小的一个
                if sheet.ncols >= 10:  # 确保至少有J列（索引9）
                    c_value = sheet.cell(row_index, 2).value  # C列是索引2
                    d_value = sheet.cell(row_index, 3).value  # D列是索引3
                    j_value = sheet.cell(row_index, 9).value  # J列是索引9
                    data_to_write.append([c_value, d_value, j_value])

    # 将数据写入CSV文件
    with open('/Users/licheng/Desktop/work/宏伟食品/宏伟食品测试/宏伟食品测试（4.26-5.8）/1600kVA/1600.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_to_write)


# 替换为你的文件夹路径
directory_path = '/Users/licheng/Desktop/work/宏伟食品/宏伟食品测试/宏伟食品测试（4.26-5.8）/1600kVA'
extract_data_from_xls(directory_path)
