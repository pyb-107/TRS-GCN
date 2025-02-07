import pandas as pd
import os

# 将一个季度的航班计划按照相同航司和机型分组
def get_airline_code(flight_no):
    """获取航司代码"""
    return flight_no[:3] if len(flight_no) == 7 else flight_no[:2]


def split_and_save_csv(input_folder, output_dir):
    """读取input文件夹下所有CSV文件，按航司代码和Type分类，每个文件保留最大文件的前15个"""
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历input文件夹下的所有CSV文件
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_folder, file_name)
            df = pd.read_csv(file_path)

            # 添加航司代码列
            df['AirlineCode'] = df['Flight No'].apply(get_airline_code)

            # 按航司代码和Type分组
            grouped = df.groupby(['AirlineCode', 'Type'])

            file_sizes = []
            file_paths = []

            # 保存拆分后的文件
            for (airline, flight_type), group in grouped:
                output_filename = f"{file_name[:-4]}_{airline}_{flight_type}.csv"
                output_file_path = os.path.join(output_dir, output_filename)
                group.to_csv(output_file_path, index=False)

                # 记录文件大小
                file_size = os.path.getsize(output_file_path)
                file_sizes.append((file_size, output_file_path))

            # 按文件大小排序，保留前15个
            file_sizes.sort(reverse=True, key=lambda x: x[0])

            # 获取需要保留的文件
            top_files = set(file_path for _, file_path in file_sizes[:15])

            # 删除其他文件
            for _, file_path in file_sizes[15:]:
                os.remove(file_path)

    print("拆分完成，每个文件保留前15个最大的拆分文件。")


# 示例调用
input_folder = "input"  # 输入CSV文件夹
output_dir = "output"  # 拆分文件存储目录
split_and_save_csv(input_folder, output_dir)
