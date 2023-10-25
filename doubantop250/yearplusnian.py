import csv

# 从控制台获取CSV文件路径
file_path = input("请输入CSV文件的路径：")

modified_rows = []

# 读取CSV文件并根据第二列的内容进行筛选和修改
with open(file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        if row[1] == "上映时间":
            year = row[2].split('-')[0]  # 提取年份
            row[2] = f"{year}年"
        modified_rows.append(row)

# 将修改后的行写入新的CSV文件
output_file_path = "modified_output.csv"
with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerows(modified_rows)

print(f"修改后的行已保存到 {output_file_path}")
