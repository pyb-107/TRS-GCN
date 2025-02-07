# -*- coding: utf-8 -*-

import pandas as pd
import os
from datetime import timedelta
from tqdm import tqdm
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
# 多线程优化

# 定义输入输出文件夹路径
input_folder = './inputdata'
output_folder = './outputdata'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 设置自定义最短衔接时间（例如，1.5小时）
min_connect_time = timedelta(hours=1.5)

def generate_all_flight_sequences_iterative(data, min_connect_time, show_progress=True):
    # 将缓存函数放在函数内部，以确保缓存仅针对当前数据集
    @lru_cache(maxsize=None)
    def get_next_flights(current_destination, current_arrival, flight_type):
        return data[(data['Origin'] == current_destination) &
                    (data['Departure Time'] >= current_arrival + min_connect_time) &
                    (data['Type'] == flight_type)]

    all_sequences = []
    stack = []

    # 初始化栈，每个元素是一个包含当前航班序列及其最后一个航班的元组
    for _, flight in data.iterrows():
        stack.append(([flight['Flight No']], flight, flight['Type']))

    # 判断是否显示进度条
    if show_progress:
        progress_bar = tqdm(total=len(stack), desc="Processing flights", unit="flight")
    else:
        progress_bar = None

    while stack:
        current_sequence, last_flight, flight_type = stack.pop()
        current_arrival = last_flight['Arrival Time']
        current_destination = last_flight['Destination']
        original_origin = data.loc[data['Flight No'] == current_sequence[0], 'Origin'].values[0]

        # 使用缓存查找下一个可以衔接的航班
        next_flights = get_next_flights(current_destination, current_arrival, flight_type)

        if next_flights.empty:
            # 如果没有找到下一个航班，检查序列首尾是否衔接
            if current_destination == original_origin:
                all_sequences.append(current_sequence)
        else:
            for _, next_flight in next_flights.iterrows():
                new_sequence = current_sequence + [next_flight['Flight No']]
                stack.append((new_sequence, next_flight, flight_type))

        # 更新进度条
        if progress_bar:
            progress_bar.update(1)

    if progress_bar:
        progress_bar.close()

    return all_sequences

def process_file(filename, show_progress=True):
    input_path = os.path.join(input_folder, filename)
    output_filename = 'paring_' + filename[len('preDeal_'):]  # 将文件名前缀改为paring_
    output_path = os.path.join(output_folder, output_filename)

    # 读取CSV文件
    data = pd.read_csv(input_path, encoding='utf-8')

    # 转换时间列为datetime类型
    data['Departure Time'] = pd.to_datetime(data['Departure Time'])
    data['Arrival Time'] = pd.to_datetime(data['Arrival Time'])

    # 生成所有航班串
    flight_sequences = generate_all_flight_sequences_iterative(data, min_connect_time, show_progress)

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

def main(show_progress=True):
    filenames = [f for f in os.listdir(input_folder) if f.startswith('preDeal_') and f.endswith('.csv')]

    # 使用ThreadPoolExecutor并行处理多个文件
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {executor.submit(process_file, filename, show_progress): filename for filename in filenames}

        # 显示进度条
        for future in as_completed(futures):
            filename = futures[future]
            try:
                future.result()  # 获取任务的结果，以便在发生异常时可以捕获
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")

if __name__ == "__main__":
    start_time = time.perf_counter()
    # 传递是否显示进度条的选项
    main(show_progress=True)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"运行时间: {elapsed_time:.6f} 秒")
