import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据文件
input_folder = "input"
file_path = os.path.join(input_folder, "preDeal_2021-3.28-2021.10.30.csv")  # 确保数据文件名正确


def load_data(file_path):
    """读取航班数据并解析成DataFrame"""
    columns = ["Flight No", "Type", "Date", "Origin", "Departure Time", "Arrival Time", "Destination", "IsDome"]
    df = pd.read_csv(file_path, header=None, names=columns, skiprows=1)

    # 提取航司代码（Flight No的前三位）
    df["Airline"] = df["Flight No"].str[:3]

    return df


def plot_stacked_bar(df):
    """绘制不同航司、不同机型的航班堆叠柱状图"""
    # 统计航班数量
    flight_counts = df.groupby(["Airline", "Type"]).size().unstack(fill_value=0)

    # 选取航班数量前15的航司
    top_airlines = flight_counts.sum(axis=1).nlargest(15).index
    flight_counts = flight_counts.loc[top_airlines]

    # 选取航班数量前7的机型，其他归为 'Other'
    top_types = flight_counts.sum().nlargest(7).index
    flight_counts["Other"] = flight_counts.drop(columns=top_types, errors='ignore').sum(axis=1)
    flight_counts = flight_counts[top_types.tolist() + ["Other"]]

    # 画图
    plt.figure(figsize=(10, 6))
    flight_counts.plot(kind='bar', stacked=True, colormap='viridis', alpha=0.85, edgecolor='black')
    # plt.title("航班数量前15的航司（按机型分类，前7大机型）")
    plt.xlabel("Airline")
    plt.ylabel("Number of flights")
    plt.xticks(rotation=45)
    plt.legend(title="aircraft type")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 显示图表
    plt.tight_layout()
    plt.show()


# 执行
if os.path.exists(file_path):
    df = load_data(file_path)
    plot_stacked_bar(df)
else:
    print(f"文件 {file_path} 不存在，请检查路径！")