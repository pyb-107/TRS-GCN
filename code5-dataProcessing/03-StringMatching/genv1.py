import os
import pandas as pd
import time
from itertools import combinations
# 初代代码，没有任何优化，使用循环遍历

def load_flights(file_path):
    """读取CSV文件并解析航班数据"""
    df = pd.read_csv(file_path)
    df = df.sort_values(by=["Departure Time"])  # 按起飞时间排序
    return df


def find_flight_sequences(flights):
    """按照规则找到所有可能的航班串"""
    sequences = []
    n = len(flights)

    # 用于存储可串接的航班链
    def find_sequences(path, last_flight):
        for i in range(n):
            flight = flights.iloc[i]

            # 确保当前航班的起飞机场与上一个航班的到达机场相同，且起飞时间满足规则
            if (flight["Origin"] == last_flight["Destination"] and
                    flight["Departure Time"] >= last_flight["Arrival Time"] and
                    (pd.to_datetime(flight["Departure Time"]) - pd.to_datetime(
                        last_flight["Arrival Time"])) >= pd.Timedelta(hours=1)):
                new_path = path + [flight]
                sequences.append(new_path)
                find_sequences(new_path, flight)

    # 遍历所有的航班，作为起始点
    for i in range(n):
        sequences.append([flights.iloc[i]])  # 单独的航班也作为航班串
        find_sequences([flights.iloc[i]], flights.iloc[i])

    return sequences


def process_flight_files(folder_path, output_folder):
    """处理文件夹中的所有CSV文件，并保存结果，同时展示处理进度和速率"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    results = {}
    total_files = len([f for f in os.listdir(folder_path) if f.endswith(".csv")])
    processed_files = 0

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            start_time = time.time()
            file_path = os.path.join(folder_path, file)
            print(f"Processing file {processed_files + 1}/{total_files}: {file}")

            flights = load_flights(file_path)
            sequences = find_flight_sequences(flights)

            formatted_sequences = []
            for seq in sequences:
                formatted_sequences.append(",".join([f["Flight No"] for f in seq]))

            results[file] = formatted_sequences

            # 计算处理时间和速率
            end_time = time.time()
            elapsed_time = end_time - start_time
            sequence_count = len(formatted_sequences)
            rate = sequence_count / elapsed_time if elapsed_time > 0 else 0
            print(f"Generated {sequence_count} sequences in {elapsed_time:.2f} seconds ({rate:.2f} sequences/sec)")

            # 保存到CSV文件
            output_file_path = os.path.join(output_folder, f"sequences_{file}")
            pd.DataFrame({"Flight Sequences": formatted_sequences}).to_csv(output_file_path, index=False)

            processed_files += 1

    return results


# 示例用法
folder_path = "./input"  # 你的CSV文件所在文件夹
output_folder = "./output"  # 存放结果的文件夹
results = process_flight_files(folder_path, output_folder)

# 打印结果
for file, sequences in results.items():
    print(f"File: {file}")
    for seq in sequences:
        print(seq)
    print("-" * 50)
