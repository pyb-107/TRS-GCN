import os
import pandas as pd
import numpy as np

# 定义输入和输出目录
input_dir = 'input'
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# 获取input目录下的所有CSV文件
csv_files = [file for file in os.listdir(input_dir) if file.endswith('.csv')]

# 定义每份的大小
split_size = 2000

for file in csv_files:
    # 读取CSV文件
    file_path = os.path.join(input_dir, file)
    df = pd.read_csv(file_path)

    # 随机打乱数据
    df = df.sample(frac=1).reset_index(drop=True)

    # 计算需要拆分的份数
    num_splits = int(np.ceil(len(df) / split_size))

    # 拆分并保存到output目录
    for i in range(num_splits):
        start_idx = i * split_size
        end_idx = min((i + 1) * split_size, len(df))
        split_df = df.iloc[start_idx:end_idx]

        # 构造文件名
        split_filename = f"{os.path.splitext(file)[0]}_part_{i + 1}.csv"
        split_filepath = os.path.join(output_dir, split_filename)

        # 保存拆分后的文件
        split_df.to_csv(split_filepath, index=False)

    print(f"Processed {file}, split into {num_splits} parts.")

print("All files processed and saved to the output directory.")
