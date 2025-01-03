import csv
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# 统计每个csv文件有多少行数据

def count_rows_in_file(csv_file):
    """
    统计单个CSV文件的数据行数（不包括标题行）。

    :param csv_file: Path对象，CSV文件路径
    :return: 文件名和行数的元组
    """
    try:
        with csv_file.open('r', encoding='utf-8') as f:
            reader = csv.reader(f)
            row_count = sum(1 for row in reader) - 1  # 减去标题行
            if row_count < 0:
                row_count = 0  # 防止文件没有数据行
        return (csv_file.name, row_count)
    except Exception as e:
        return (csv_file.name, f"错误: {e}")


def count_csv_rows_multithreaded(directory='inputdata', max_workers=4):
    """
    使用多进程统计指定目录下所有CSV文件的数据行数，并按文件名排序输出。

    :param directory: 要扫描的目录，默认为 'inputdata'
    :param max_workers: 最大并发进程数，默认为4
    :return: 无，打印每个CSV文件的行数（按文件名排序）
    """
    path = Path(directory)

    # 检查目录是否存在
    if not path.exists():
        print(f"目录 '{directory}' 不存在。请确保该目录存在于当前工作目录中。")
        return

    # 查找所有以 .csv 结尾的文件
    csv_files = list(path.glob('*.csv'))

    if not csv_files:
        print(f"目录 '{directory}' 下没有找到CSV文件。")
        return

    print(f"找到 {len(csv_files)} 个CSV文件在 '{directory}' 目录下:\n")

    results = []  # 用于存储所有统计结果

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有CSV文件的统计任务
        future_to_file = {executor.submit(count_rows_in_file, csv_file): csv_file for csv_file in csv_files}

        # 处理已完成的任务，并收集结果
        for future in as_completed(future_to_file):
            file_name, row_count = future.result()
            results.append((file_name, row_count))

    # 按文件名排序结果
    results_sorted = sorted(results, key=lambda x: x[0])

    # 打印排序后的结果
    for file_name, row_count in results_sorted:
        print(f"文件: {file_name} - 数据行数: {row_count}")


if __name__ == "__main__":
    count_csv_rows_multithreaded()
