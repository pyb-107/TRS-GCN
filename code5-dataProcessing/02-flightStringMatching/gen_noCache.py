# -*- coding: utf-8 -*-

import pandas as pd
import os
from datetime import timedelta
from tqdm import tqdm
import time

start_time = time.time()  # 记录开始时间
# 定义输入输出文件夹路径
input_folder = './inputdata'
output_folder = './outputdata'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 设置自定义最短衔接时间（例如，1.5小时）
min_connect_time = timedelta(hours=2)

def get_next_flights(current_destination, current_arrival, flight_type, data):
    return data[(data['Origin'] == current_destination) &
                (data['Departure Time'] >= current_arrival + min_connect_time) &
                (data['Type'] == flight_type)]

def generate_all_flight_sequences_iterative(data, min_connect_time):
    all_sequences = []
    stack = []

    # 初始化栈，每个元素是一个包含当前航班序列及其最后一个航班的元组
    for _, flight in data.iterrows():
        # 单独航班本身可以构成一条合法的航班串
        all_sequences.append([flight['Flight No']])
        stack.append(([flight['Flight No']], flight, flight['Type']))

    # 使用栈迭代代替递归，增加进度条显示
    with tqdm(total=len(stack), desc="Processing flights", unit="flight") as pbar:
        while stack:
            current_sequence, last_flight, flight_type = stack.pop()
            current_arrival = last_flight['Arrival Time']
            current_destination = last_flight['Destination']
            original_origin = data.loc[data['Flight No'] == current_sequence[0], 'Origin'].values[0]

            # 查找下一个可以衔接的航班
            next_flights = get_next_flights(current_destination, current_arrival, flight_type, data)

            if next_flights.empty:
                # 如果没有找到下一个航班，检查序列首尾是否衔接
                if current_destination == original_origin:
                    if current_sequence not in all_sequences:
                        all_sequences.append(current_sequence)
            else:
                for _, next_flight in next_flights.iterrows():
                    new_sequence = current_sequence + [next_flight['Flight No']]
                    stack.append((new_sequence, next_flight, flight_type))
            # 更新进度条
            pbar.update(1)

    return all_sequences

# 遍历inputdata文件夹下的所有以preDeal_为前缀的CSV文件
for filename in os.listdir(input_folder):
    if filename.startswith('preDeal_') and filename.endswith('.csv'):
        input_path = os.path.join(input_folder, filename)
        output_filename = 'paring_' + filename[len('preDeal_'):]  # 将文件名前缀改为paring_
        output_path = os.path.join(output_folder, output_filename)

        # 读取CSV文件
        data = pd.read_csv(input_path)

        # 转换时间列为datetime类型
        data['Departure Time'] = pd.to_datetime(data['Departure Time'])
        data['Arrival Time'] = pd.to_datetime(data['Arrival Time'])

        # 生成所有航班串
        flight_sequences = generate_all_flight_sequences_iterative(data, min_connect_time)

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

        print(f"处理完成并保存到 {output_path}")

end_time = time.time()    # 记录结束时间
elapsed_time = end_time - start_time  # 计算运行时间
print(f"运行时间: {elapsed_time:.6f} 秒")