import csv

# 从控制台获取CSV文件路径
file_path = input("请输入CSV文件的路径：")

years = []

# 读取CSV文件并提取每一行的前四位年份
with open(file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        year = row[0][:4]  # 获取前四位作为年份
        years.append(year)

# 将年份写入新的CSV文件
output_file_path = "extracted_years.csv"
with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    for year in years:
        writer.writerow([year])

print(f"年份已保存到 {output_file_path}")
