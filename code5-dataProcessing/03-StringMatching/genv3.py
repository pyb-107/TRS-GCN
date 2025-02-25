import os
import pandas as pd
import time
import bisect
from datetime import datetime

# 记录代码开始执行的时间
start_total_time = time.time()

def load_flights(file_path):
    """读取CSV文件并解析航班数据，预处理后续连接"""
    df = pd.read_csv(file_path)
    df["Departure Time"] = pd.to_datetime(df["Departure Time"])
    df["Arrival Time"] = pd.to_datetime(df["Arrival Time"])
    df = df.sort_values(by=["Departure Time"])  # 按起飞时间排序

    flight_list = df.to_dict('records')
    departure_times = df["Departure Time"].tolist()
    next_flights = {}  # 存储每个航班的后续航班索引

    for i, flight in enumerate(flight_list):
        # 计算允许的最小后续起飞时间（当前到达时间 + 1小时）
        min_departure = flight["Arrival Time"] + pd.Timedelta(hours=1)
        # 使用二分查找确定起始位置
        start_idx = bisect.bisect_left(departure_times, min_departure)

        # 收集所有符合条件的后续航班
        valid_next = []
        for j in range(start_idx, len(flight_list)):
            if flight_list[j]["Origin"] == flight["Destination"]:
                valid_next.append(j)

        next_flights[i] = valid_next

    return flight_list, next_flights


def find_flight_sequences(flight_list, next_flights):
    """使用迭代方式生成所有合法航班序列"""
    sequences = []
    stack = []

    # 初始化栈，每个航班作为独立序列的起点
    for i in range(len(flight_list)):
        stack.append([i])
        sequences.append([i])

    # 使用栈迭代处理
    while stack:
        current_path = stack.pop()
        last_idx = current_path[-1]

        # 遍历所有后续航班
        for next_idx in next_flights.get(last_idx, []):
            new_path = current_path + [next_idx]
            sequences.append(new_path)
            stack.append(new_path)

    return sequences


def process_flight_files(folder_path, output_folder):
    """处理文件夹中的所有CSV文件，并保存结果"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_files = len([f for f in os.listdir(folder_path) if f.endswith(".csv")])
    processed_files = 0

    for file in os.listdir(folder_path):
        if not file.endswith(".csv"):
            continue

        start_time = time.time()
        file_path = os.path.join(folder_path, file)
        print(f"Processing {processed_files + 1}/{total_files}: {file}")

        # 加载数据并预处理
        flight_list, next_flights = load_flights(file_path)

        # 生成所有航班序列
        sequences = find_flight_sequences(flight_list, next_flights)

        # 格式化输出为 'Duty Period #, Flights' 形式
        formatted = [
            f"{idx + 1},\"{str([flight_list[i]['Flight No'] for i in seq])}\""
            for idx, seq in enumerate(sequences)
        ]

        # 修改输出文件名的格式：将 "preDeal_" 改为 "paring_"
        output_file_name = file.replace("preDeal_", "paring_")
        output_path = os.path.join(output_folder, output_file_name)

        # 保存结果
        with open(output_path, "w") as output_file:
            output_file.write("Duty Period #,Flights\n")  # 写入标题行
            output_file.write("\n".join(formatted))  # 写入所有的序列

        # 性能统计
        elapsed = time.time() - start_time
        print(f"生成 {len(formatted)} 条序列，耗时 {elapsed:.2f} 秒 ({(len(formatted) / elapsed):.1f} 条/秒)")

        processed_files += 1


# 使用示例
folder_path = "./input"
output_folder = "./output"
process_flight_files(folder_path, output_folder)

# 记录代码结束执行的时间
end_total_time = time.time()

# 计算总执行时间
total_elapsed_time = end_total_time - start_total_time

# 打印总执行时间
print(f"代码总执行时间: {total_elapsed_time:.2f} 秒")