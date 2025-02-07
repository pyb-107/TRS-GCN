import os
import time
import pandas as pd
from collections import defaultdict


def load_flights(file_path):
    """
    读取CSV文件并解析航班数据，返回（DataFrame, 航班列表）。
    """
    df = pd.read_csv(file_path)
    df["Departure Time"] = pd.to_datetime(df["Departure Time"])
    df["Arrival Time"] = pd.to_datetime(df["Arrival Time"])
    df = df.sort_values(by=["Departure Time"]).reset_index(drop=True)

    flights_list = []
    for i, row in df.iterrows():
        flights_list.append({
            'index': i,
            'flight_no': row["Flight No"],
            'origin': row["Origin"],
            'destination': row["Destination"],
            'dep_time': row["Departure Time"],
            'arr_time': row["Arrival Time"]
        })

    return df, flights_list


def build_adjacency_list(flights_list):
    """
    构建邻接表 adjacency，其中 adjacency[i] 是一个列表，
    记录可以衔接的航班索引。
    """
    n = len(flights_list)
    adjacency = [[] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if (flights_list[j]['origin'] == flights_list[i]['destination'] and
                    flights_list[j]['dep_time'] >= flights_list[i]['arr_time'] and
                    (flights_list[j]['dep_time'] - flights_list[i]['arr_time']).total_seconds() >= 3600):
                adjacency[i].append(j)

    return adjacency


def find_flight_sequences_iterative(adjacency, start_index, memo):
    """
    使用迭代 + 栈的方式，从 start_index 出发寻找所有可衔接的航班序列。
    """
    if start_index in memo:
        return memo[start_index]

    all_sequences = []
    stack = [(start_index, [start_index])]

    while stack:
        current_node, current_path = stack.pop()
        all_sequences.append(current_path)

        for next_node in adjacency[current_node]:
            stack.append((next_node, current_path + [next_node]))

    memo[start_index] = all_sequences
    return all_sequences


def find_all_sequences_for_flights(flights_list):
    """
    主函数：构建邻接表 + 迭代搜索所有航班串。
    """
    adjacency = build_adjacency_list(flights_list)
    memo = {}
    all_sequences = []

    for i in range(len(flights_list)):
        sequences_from_i = find_flight_sequences_iterative(adjacency, i, memo)
        all_sequences.extend(sequences_from_i)

    return all_sequences


def process_flight_files(folder_path, output_folder):
    """处理所有CSV文件，并记录处理时间"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    results = {}
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    total_files = len(files)

    start_time_all = time.time()  # 记录所有文件的处理起始时间

    for idx, file in enumerate(files, start=1):
        file_start_time = time.time()  # 记录单个文件处理起始时间
        file_path = os.path.join(folder_path, file)
        print(f"Processing {idx}/{total_files}: {file}")

        df, flights_list = load_flights(file_path)
        all_sequences_idx = find_all_sequences_for_flights(flights_list)

        formatted_sequences = []
        for seq in all_sequences_idx:
            flight_nos = [flights_list[idx]['flight_no'] for idx in seq]
            formatted_sequences.append(",".join(flight_nos))

        results[file] = formatted_sequences

        # 计算处理时间和速率
        file_end_time = time.time()
        elapsed_time = file_end_time - file_start_time
        sequence_count = len(formatted_sequences)
        rate = sequence_count / elapsed_time if elapsed_time > 0 else 0

        print(f"生成 {sequence_count} 条序列，耗时 {elapsed_time:.2f} 秒 ({rate:.1f} 条/秒)")

        # 保存到CSV文件
        output_file_path = os.path.join(output_folder, f"sequences_{file}")
        pd.DataFrame({"Flight Sequences": formatted_sequences}).to_csv(output_file_path, index=False)

    # 计算总耗时
    end_time_all = time.time()
    total_elapsed_time = end_time_all - start_time_all
    print(f"\n所有文件处理完毕，总耗时 {total_elapsed_time:.2f} 秒")

    return results


if __name__ == "__main__":
    folder_path = "./input"  # CSV 文件所在文件夹
    output_folder = "./output"  # 结果存放文件夹
    results = process_flight_files(folder_path, output_folder)
