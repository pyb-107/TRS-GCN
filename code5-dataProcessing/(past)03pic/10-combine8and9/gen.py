import os
import matplotlib.pyplot as plt

# 画正确率和错误率随阈值变化曲线
def calculate_ratios(numbers_a, numbers_b):
    # 计算 A 文件覆盖 B 文件的数字占比
    covered_numbers = numbers_a.intersection(numbers_b)
    coverage_ratio = len(covered_numbers) / len(numbers_b) if numbers_b else 0

    # 计算 A 文件中未出现在 B 文件的数字占 A 文件数字总量的比例
    non_covered_numbers = numbers_a - numbers_b
    non_coverage_ratio = len(non_covered_numbers) / len(numbers_a) if numbers_a else 0

    return coverage_ratio, non_coverage_ratio


# 示例文件路径
input_prob_file = 'input/sample_0.prob'
sol_file = 'input/0.sol'

# 读取文件 B 中的数字
with open(sol_file, 'r') as file_b:
    numbers_b = set(int(line.strip()) for line in file_b if line.strip())

# 设置阈值范围和计算间隔
start_threshold = 0.0
end_threshold = 1.0
step = 0.02  # 可自定义计算间隔

thresholds = []
current_threshold = start_threshold
while current_threshold <= end_threshold:
    thresholds.append(current_threshold)
    current_threshold += step

coverage_ratios = []
non_coverage_ratios = []

# 确保 output 文件夹存在
output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_file_path = os.path.join(output_folder, 'threshold_stats.csv')
with open(output_file_path, 'w') as output_file:
    output_file.write('阈值,A 文件覆盖 B 文件的数字占比,A 文件中未出现在 B 文件的数字占 A 文件数字总量的比例\n')

    for threshold in thresholds:
        # 读取文件 A 中的数字并根据阈值筛选
        numbers_a = set()
        with open(input_prob_file, 'r') as input_file:
            for line in input_file:
                parts = line.strip().split()
                if len(parts) == 2:
                    number, value = parts
                    try:
                        value = float(value)
                        if value >= threshold:
                            numbers_a.add(int(number))
                    except ValueError:
                        continue

        # 计算比例
        coverage_ratio, non_coverage_ratio = calculate_ratios(numbers_a, numbers_b)
        coverage_ratios.append(coverage_ratio)
        non_coverage_ratios.append(non_coverage_ratio)

        print(f"阈值: {threshold:.1f}, A 文件覆盖 B 文件的数字占比: {coverage_ratio * 100:.2f}%, A 文件中未出现在 B 文件的数字占比: {non_coverage_ratio * 100:.2f}%")
        output_file.write(f'{threshold:.1f},{coverage_ratio:.4f},{non_coverage_ratio:.4f}\n')

# 绘制统计图
plt.figure(figsize=(10, 6))
plt.plot(thresholds, coverage_ratios, label='A 文件覆盖 B 文件的数字占比')
plt.plot(thresholds, non_coverage_ratios, label='A 文件中未出现在 B 文件的数字占 A 文件数字总量的比例')
plt.xlabel('阈值')
plt.ylabel('比例')
plt.title('不同阈值下的比例变化情况')
plt.legend()
plt.grid(True)
plt.show()