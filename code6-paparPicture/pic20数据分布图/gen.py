import os
import matplotlib.pyplot as plt


def count_lines_in_file(file_path):
    """计算单个文件的总行数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except Exception as e:
        print(f"无法读取文件 {file_path}: {e}")
        return None  # 读取失败则返回 None


def analyze_line_distribution(input_folder):
    """统计input目录下所有文件的行数分布情况"""
    line_counts = {}
    all_lines = []

    # 遍历 input 目录下所有文件
    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)

        if os.path.isfile(file_path):  # 确保是文件
            line_count = count_lines_in_file(file_path)
            if line_count is not None:
                line_counts[file] = line_count
                all_lines.append(line_count)

    if not all_lines:
        print("未找到有效文件或文件为空")
        return [], []  # 返回空的结果

    return line_counts, all_lines


# 读取 input1 和 input2 数据
input_folder1 = "./input1"
input_folder2 = "./input2"

line_counts1, all_lines1 = analyze_line_distribution(input_folder1)
line_counts2, all_lines2 = analyze_line_distribution(input_folder2)

if not all_lines1 or not all_lines2:
    print("无法读取数据，程序终止。")
else:
    # 绘制并排显示两个直方图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # 第一个直方图（input1）
    ax1.hist(all_lines1, bins=20, edgecolor='black', color='skyblue', alpha=0.75)
    # ax1.set_title("Input1 文件行数分布")
    ax1.set_xlabel("Flight num")
    ax1.set_ylabel("Group Num")
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # 第二个直方图（input2）
    ax2.hist(all_lines2, bins=20, edgecolor='black', color='lightgreen', alpha=0.75)
    # ax2.set_title("Input2 文件行数分布")
    ax2.set_xlabel("String num")
    ax2.set_ylabel("Group Num")
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()  # 自动调整子图间距
    plt.show()

    # 打印每个文件的行数（可选）
    print("\n📄 Input1 每个文件的行数:")
    for file, count in sorted(line_counts1.items(), key=lambda x: x[1], reverse=True):
        print(f"{file}: {count} 行")

    print("\n📄 Input2 每个文件的行数:")
    for file, count in sorted(line_counts2.items(), key=lambda x: x[1], reverse=True):
        print(f"{file}: {count} 行")
