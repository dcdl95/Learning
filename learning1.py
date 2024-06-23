import numpy as np
# 创建数组
arr = np.array([1, 2, 3, 4, 5])
print(arr)  # 输出 [1 2 3 4 5]

print("****")

matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix)
# 输出
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]
print("****")
# 数组运算
arr2 = arr * 2
print(arr2)  # 输出 [ 2  4  6  8 10]
print("****")
# 数组形状
print(matrix.shape)  # 输出 (3, 3)
print("****")
# 数组转置
print(matrix.T)
# 输出
# [[1 4 7]
#  [2 5 8]
#  [3 6 9]]
print("****")
# 生成随机数
rand_nums = np.random.random((3, 3))
print(rand_nums)
print("****")

# 数组元素求和
total_sum = np.sum(matrix)
print(total_sum)  # 输出 45
print("****")
# 数组元素的均值
mean_val = np.mean(matrix)
print(mean_val)  # 输出 5.0
print("****")
# 数组元素的标准差
std_val = np.std(matrix)
print(std_val)  # 输出 2.581988897471611
print("****")
# 数组元素的最大值和最小值
max_val = np.max(matrix)
min_val = np.min(matrix)
print(max_val, min_val)  # 输出 9 1
print("****")
print("hello china")
print(std_val)