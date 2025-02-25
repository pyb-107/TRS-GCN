# 统计正确率和错误率
def calculate_ratios(file_a_path, file_b_path):
    # 读取文件 A 中的数字
    with open(file_a_path, 'r') as file_a:
        numbers_a = set(int(line.strip()) for line in file_a if line.strip())

    # 读取文件 B 中的数字
    with open(file_b_path, 'r') as file_b:
        numbers_b = set(int(line.strip()) for line in file_b if line.strip())

    # 计算 A 文件覆盖 B 文件的数字占比
    covered_numbers = numbers_a.intersection(numbers_b)
    coverage_ratio = len(covered_numbers) / len(numbers_b) if numbers_b else 0

    # 计算 A 文件中未出现在 B 文件的数字占 A 文件数字总量的比例
    non_covered_numbers = numbers_a - numbers_b
    non_coverage_ratio = len(non_covered_numbers) / len(numbers_a) if numbers_a else 0

    return coverage_ratio, non_coverage_ratio

# 示例文件路径，你需要将其替换为实际的文件路径
file_a_path = 'sample_0_processed.prob'
file_b_path = '0.sol'

coverage_ratio, non_coverage_ratio = calculate_ratios(file_a_path, file_b_path)
print(f"A 文件覆盖 B 文件的数字占比: {coverage_ratio * 100:.2f}%")
print(f"A 文件中未出现在 B 文件的数字占 A 文件数字总量的比例: {non_coverage_ratio * 100:.2f}%")