# -*- coding: utf-8 -*-

import pandas as pd
import os
from datetime import timedelta
from tqdm import tqdm
from functools import lru_cache
import time

# 定义输入输出文件夹路径
input_folder = './inputdata'
output_folder = './outputdata'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 设置自定义最短衔接时间（例如，1.5小时）
min_connect_time = timedelta(hours=1)


@lru_cache(maxsize=None)
def get_next_flights(current_destination, current_arrival, flight_type, current_carrier):
    return data[(data['Origin'] == current_destination) &
                (data['Departure Time'] >= current_arrival + min_connect_time) &
                (data['Type'] == flight_type) &
                (data['Flight No'].str[:2] == current_carrier)]


def generate_all_flight_sequences_iterative(data, min_connect_time):
    all_sequences = []
    stack = []

    # 初始化栈，每个元素是一个包含当前航班序列及其最后一个航班的元组
    for _, flight in data.iterrows():
        all_sequences.append([flight['Flight No']])
        stack.append(([flight['Flight No']], flight, flight['Type'], flight['Flight No'][:2]))  # 添加航司信息

    # 使用栈迭代代替递归，增加进度条显示
    with tqdm(total=len(stack), desc="Processing flights", unit="flight") as pbar:
        while stack:
            current_sequence, last_flight, flight_type, current_carrier = stack.pop()
            current_arrival = last_flight['Arrival Time']
            current_destination = last_flight['Destination']

            # 使用缓存查找下一个可以衔接的航班
            next_flights = get_next_flights(current_destination, current_arrival, flight_type, current_carrier)

            if next_flights.empty:
                if current_sequence not in all_sequences:
                    all_sequences.append(current_sequence)
            else:
                for _, next_flight in next_flights.iterrows():
                    new_sequence = current_sequence + [next_flight['Flight No']]
                    stack.append((new_sequence, next_flight, flight_type, current_carrier))

            pbar.update(1)

    return all_sequences


# 遍历inputdata文件夹下的所有以preDeal_为前缀的CSV文件
for filename in os.listdir(input_folder):
    if filename.startswith('preDeal_') and filename.endswith('.csv'):
        input_path = os.path.join(input_folder, filename)
        output_filename = 'paring_' + filename[len('preDeal_'):]  # 将文件名前缀改为paring_
        output_path = os.path.join(output_folder, output_filename)

        # 记录文件开始处理的时间
        file_start_time = time.time()

        # 读取CSV文件
        data = pd.read_csv(input_path)

        # 转换时间列为datetime类型
        data['Departure Time'] = pd.to_datetime(data['Departure Time'])
        data['Arrival Time'] = pd.to_datetime(data['Arrival Time'])

        # 记录初始航班数
        initial_flight_count = len(data)
        print(f"处理文件: {filename}，初始航班数: {initial_flight_count}")

        # 生成所有航班串
        flight_sequences = generate_all_flight_sequences_iterative(data, min_connect_time)

        # 记录生成的航班串数量
        sequence_count = len(flight_sequences)
        print(f"文件 {filename} 计算完成，生成航班串数量: {sequence_count}")

        # 计算文件处理时间
        file_end_time = time.time()
        file_elapsed_time = file_end_time - file_start_time
        print(f"文件 {filename} 计算耗时: {file_elapsed_time:.6f} 秒")

        # 构建输出数据格式
        output_data = []
        for i, seq in enumerate(flight_sequences, start=1):
            output_data.append({
                'Duty Period #': i,
                'Flights': str(seq)
            })

        # 转换为DataFrame
        output_df = pd.DataFrame(output_data)

        # 将结果保存为CSV文件
        output_df.to_csv(output_path, index=False)

        print(f"文件 {filename} 处理完成并保存到 {output_path}")

# 记录总运行时间
end_time = time.time()
elapsed_time = end_time - file_start_time
print(f"总运行时间: {elapsed_time:.6f} 秒")
