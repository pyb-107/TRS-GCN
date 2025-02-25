import numpy as np
import matplotlib.pyplot as plt
import os

# 读取真实标签文件
def read_labels(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        # 假设元素总数，这里可根据实际情况修改，如果已知最大序号可以直接指定
        max_num = max(int(line.strip()) for line in lines) if lines else 0
        labels = np.zeros(max_num)
        for line in lines:
            idx = int(line.strip()) - 1  # 序号从 1 开始，转换为 0 索引
            labels[idx] = 1
    return labels

# 读取预测概率文件
def read_probabilities(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        probs = []
        for line in lines:
            idx, prob = line.strip().split()
            probs.append(float(prob))
    return np.array(probs)

# 根据 t 值设置概率最小的 t% 个元素为 0
def set_min_probs_to_zero(probs, t):
    sorted_indices = np.argsort(probs)
    num_to_set_zero = int(len(probs) * t / 100)
    new_probs = probs.copy()
    new_probs[sorted_indices[:num_to_set_zero]] = 0
    return new_probs

# 计算准确率，只针对概率最小的 t% 个元素
def calculate_accuracy(labels, probs, t):
    sorted_indices = np.argsort(probs)
    num_to_check = int(len(probs) * t / 100)
    selected_indices = sorted_indices[:num_to_check]
    selected_labels = labels[selected_indices]
    selected_predictions = (probs[selected_indices] >= 0.5).astype(int)
    if num_to_check == 0:
        return 1.0  # 如果 t 为 0，认为准确率为 100%
    accuracy = np.mean(selected_predictions == selected_labels)
    return accuracy

# 主函数
def main():
    input_dir = 'input'
    # 获取所有的索引，假设标签文件和概率文件的索引是连续的
    file_indices = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.sol'):
            try:
                index = int(file_name.split('.')[0])
                file_indices.append(index)
            except ValueError:
                continue
    file_indices.sort()

    # 生成 t 值，0 - 10% 更密集，去掉零点，范围限制在 0 - 50
    t_values_0_10 = np.linspace(0.1, 10, 20)  # 0.1 到 10 之间取 20 个点
    t_values_10_50 = np.arange(11, 51, 1)
    t_values = np.concatenate((t_values_0_10, t_values_10_50))

    all_accuracies = []

    # 遍历每个索引对应的文件对
    for index in file_indices:
        label_file = os.path.join(input_dir, f'{index}.sol')
        prob_file = os.path.join(input_dir, f'sample_{index}.prob')

        # 读取文件
        labels = read_labels(label_file)
        probs = read_probabilities(prob_file)

        # 确保标签和概率数组长度一致
        if len(labels) < len(probs):
            labels = np.pad(labels, (0, len(probs) - len(labels)), 'constant', constant_values=0)

        accuracies = []
        # 计算不同 t 值下的准确率
        for t in t_values:
            new_probs = set_min_probs_to_zero(probs, t)
            accuracy = calculate_accuracy(labels, new_probs, t)
            accuracies.append(accuracy)

        all_accuracies.append(accuracies)

    # 计算所有文件的准确率平均值
    average_accuracies = np.mean(all_accuracies, axis=0)

    # 绘制统计图
    plt.plot(t_values, average_accuracies, marker='o')
    plt.xlabel('t (%)')
    plt.ylabel('Average Accuracy')
    plt.title('problem size 10000-20000')
    plt.xlim(0, 50)
    # 设置 y 轴范围，这里假设范围是 0 到 1
    plt.ylim(0.95, 1)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()