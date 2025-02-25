import os
# 根据设定的阈值，输出解
# 设定阈值
threshold = 0.5

# 输入文件夹和输出文件夹路径
input_folder = 'input'
output_folder = 'output'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取输入文件夹中的所有 .prob 文件
prob_files = [f for f in os.listdir(input_folder) if f.endswith('.prob')]

for prob_file in prob_files:
    input_file_path = os.path.join(input_folder, prob_file)
    output_file_name = os.path.splitext(prob_file)[0] + '_processed.prob'
    output_file_path = os.path.join(output_folder, output_file_name)

    # 读取文件并处理
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            # 分割每行数据
            parts = line.strip().split()
            if len(parts) == 2:
                number, value = parts
                # 将值转换为浮点数
                try:
                    value = float(value)
                    # 检查是否满足阈值条件
                    if value >= threshold:
                        # 写入第一列的值到输出文件
                        output_file.write(f"{number}\n")
                except ValueError:
                    continue

    print(f"处理完成: {prob_file}，结果已保存到 {output_file_path}")