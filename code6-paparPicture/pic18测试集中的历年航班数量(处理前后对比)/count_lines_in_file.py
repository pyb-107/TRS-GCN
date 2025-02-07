import os


def count_lines_in_file(file_path):
    """统计文件的行数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except Exception as e:
        print(f"无法读取文件 {file_path}: {e}")
        return None


def count_lines_in_directory(directory):
    """统计目录中所有文件的行数"""
    line_counts = {}
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在")
        return line_counts

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            line_count = count_lines_in_file(file_path)
            if line_count is not None:
                line_counts[filename] = line_count

    return line_counts


def save_results(results, output_file="line_counts.txt"):
    """将统计结果保存到文件中"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for filename, line_count in results.items():
            f.write(f"{filename}: {line_count} 行\n")
    print(f"统计结果已保存到 {output_file}")


if __name__ == "__main__":
    input_directory = "input"
    results = count_lines_in_directory(input_directory)
    save_results(results)
