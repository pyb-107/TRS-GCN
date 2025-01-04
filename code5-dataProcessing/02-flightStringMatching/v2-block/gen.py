import networkx as nx
import pandas as pd
import os
from datetime import timedelta
import time
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

# 缓存优化
# 定义输入输出文件夹路径
start_time = time.time()  # 记录开始时间
input_folder = './inputdata'
output_folder = './outputdata'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 设置自定义最短衔接时间（例如，1.5小时）
min_connect_time = timedelta(hours=1)


@lru_cache(maxsize=None)
def get_next_flights(current_destination, current_arrival, flight_type):
    return data[(data['Origin'] == current_destination) &
                (data['Departure Time'] >= current_arrival + min_connect_time) &
                (data['Type'] == flight_type)]


def partition_data(data, num_blocks=4):
    """根据起飞时间将数据分为若干块"""
    data_sorted = data.sort_values('Departure Time')
    block_size = len(data) // num_blocks
    blocks = [data_sorted.iloc[i * block_size: (i + 1) * block_size] for i in range(num_blocks)]
    return blocks


def dynamic_programming_block(block_data, min_connect_time):
    """
    对每个块内的航班进行动态规划计算，使用图结构来表示航班的衔接。
    """
    # 按照航班的出发时间排序
    block_data = block_data.sort_values('Departure Time')

    # 初始化图
    G = nx.DiGraph()

    # 将航班添加到图中，节点是航班编号
    for _, flight in block_data.iterrows():
        G.add_node(flight['Flight No'], flight=flight)

    # 构建航班之间的衔接关系（边）
    for i, flight_i in block_data.iterrows():
        for j, flight_j in block_data.iterrows():
            if i >= j:
                continue  # 防止自己与自己衔接以及反向遍历
            # 判断航班i是否可以与航班j衔接
            if flight_j['Departure Time'] >= flight_i['Arrival Time'] + min_connect_time:
                G.add_edge(flight_i['Flight No'], flight_j['Flight No'])

    # 使用动态规划计算最优的航班衔接序列
    # dp 存储每个航班的最优序列，prev 存储前一个航班的编号
    dp = {}  # 每个航班的最大长度
    prev = {}  # 存储每个航班的前驱航班编号
    max_seq_end = None  # 最长序列的最后一个航班

    # 遍历图中的每个节点（航班）
    for flight in block_data['Flight No']:
        dp[flight] = 1  # 每个航班的初始序列长度为1
        prev[flight] = None  # 初始没有前驱航班

    # 从图中节点遍历，计算每个航班的最优路径
    for flight_i in block_data['Flight No']:
        for flight_j in G.neighbors(flight_i):
            if dp[flight_j] < dp[flight_i] + 1:
                dp[flight_j] = dp[flight_i] + 1
                prev[flight_j] = flight_i

    # 找到最大序列的最后一个航班
    max_length = max(dp.values())
    max_seq_end = [flight for flight, length in dp.items() if length == max_length][0]

    # 反向追溯最优路径
    longest_sequence = []
    while max_seq_end is not None:
        longest_sequence.append(max_seq_end)
        max_seq_end = prev[max_seq_end]

    # 返回按顺序排列的最优航班序列
    longest_sequence.reverse()

    # 生成所有可能的航班串
    flight_sequences = []
    for flight in block_data['Flight No']:
        # 从每个航班开始计算最优路径
        current_sequence = []
        current_flight = flight
        while current_flight is not None:
            current_sequence.append(current_flight)
            current_flight = prev.get(current_flight, None)
        current_sequence.reverse()  # 翻转回正确的顺序
        flight_sequences.append(current_sequence)

    return flight_sequences


def merge_blocks(blocks):
    """
    合并不同块的结果，处理跨块的航班衔接。

    :param blocks: 一个包含多个块的列表，每个块是一个航班序列。
    :param min_connect_time: 最短衔接时间。
    :return: 合并后的航班序列。
    """
    merged_sequences = []

    for i in range(len(blocks) - 1):
        block_a = blocks[i]
        block_b = blocks[i + 1]

        # 获取最后一个航班的到达时间和第一个航班的起飞时间
        last_flight_in_a = block_a[-1]
        first_flight_in_b = block_b[0]

        last_arrival_time = last_flight_in_a['Arrival Time']
        first_departure_time = first_flight_in_b['Departure Time']

        # 判断是否可以衔接
        if first_departure_time >= last_arrival_time + min_connect_time:
            # 如果可以衔接，就合并两个块的序列
            merged_sequences.append(block_a + block_b)
        else:
            # 如果不能衔接，独立处理每个块
            merged_sequences.append(block_a)
            merged_sequences.append(block_b)

    # 处理最后一个块
    if len(blocks) > 0:
        merged_sequences.append(blocks[-1])

    return merged_sequences


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

        # 分块
        blocks = partition_data(data, num_blocks=4)

        # 使用多线程并行计算每个块的航班衔接序列
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(dynamic_programming_block, block, min_connect_time) for block in blocks]
            block_results = [future.result() for future in futures]

        # 合并块结果
        all_sequences = merge_blocks(block_results)

        # 构建输出数据格式
        output_data = []
        for i, seq in enumerate(all_sequences, start=1):
            output_data.append({
                'Duty Period #': i,
                'Flights': str(seq)
            })

        # 转换为DataFrame
        output_df = pd.DataFrame(output_data)

        # 将结果保存为CSV文件
        output_df.to_csv(output_path, index=False)

        print(f"处理完成并保存到 {output_path}")

end_time = time.time()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算运行时间
print(f"运行时间: {elapsed_time:.6f} 秒")
