import csv
from collections import defaultdict

# 从控制台获取CSV文件路径
file_path = input("请输入CSV文件的路径：")

# 读取CSV文件
with open(file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    data = list(reader)


# 使用字典按第二列的内容进行分类
data_dict = defaultdict(list)
for row in data:
    key = row[1]  # 第二列作为键
    data_dict[key].append(row)

# 将分类后的数据写入新的CSV文件
for key, rows in data_dict.items():
    with open(f'{key}.csv', 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(rows)

