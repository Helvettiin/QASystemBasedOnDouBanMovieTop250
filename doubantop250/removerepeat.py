import csv

# 从控制台获取CSV文件路径
file_path = input("请输入CSV文件的路径：")

unique_items = set()

# 读取CSV文件并提取第三列中的不重复项
with open(file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        unique_items.add(row[2])  # 第三列的数据

# 将不重复的项写入新的CSV文件
output_file_path = "unique_items.csv"
with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    for item in unique_items:
        writer.writerow([item])

print(f"不重复的项已保存到 {output_file_path}")
