import csv

# 从控制台获取CSV文件路径
file_path = input("请输入CSV文件的路径：")

filtered_rows = []

# 读取CSV文件并根据第二列的内容进行筛选
with open(file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        if row[1] != "剧情简介":
            filtered_rows.append(row)

# 将筛选后的行写入新的CSV文件
output_file_path = "filtered_output.csv"
with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerows(filtered_rows)

print(f"筛选后的行已保存到 {output_file_path}")
