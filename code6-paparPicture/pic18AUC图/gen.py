import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import os

def load_prob_file(file_path):
    """
    加载以.prob结尾的预测结果文件
    :param file_path: 文件路径
    :return: 样本序号列表和对应的预测概率列表
    """
    indices = []
    probs = []
    with open(file_path, 'r') as f:
        for line in f:
            index, prob = line.strip().split()
            indices.append(int(index))
            probs.append(float(prob))
    return indices, probs

def load_sol_file(file_path):
    """
    加载以.sol结尾的标签文件
    :param file_path: 文件路径
    :return: 正样本的序号集合
    """
    positive_indices = set()
    with open(file_path, 'r') as f:
        for line in f:
            positive_indices.add(int(line.strip()))
    return positive_indices

def get_true_labels(indices, positive_indices):
    """
    根据样本序号和正样本序号集合生成真实标签
    :param indices: 样本序号列表
    :param positive_indices: 正样本的序号集合
    :return: 真实标签列表
    """
    true_labels = [1 if index in positive_indices else 0 for index in indices]
    return true_labels

def plot_roc_curve(ax, true_labels, probs, file_name):
    """
    绘制ROC图并计算AUC
    :param ax: 子图对象
    :param true_labels: 真实标签列表
    :param probs: 预测概率列表
    :param file_name: 文件名，用于图的标题
    """
    fpr, tpr, _ = roc_curve(true_labels, probs)
    roc_auc = auc(fpr, tpr)

    ax.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title(f'Receiver operating characteristic for size {file_name}')
    ax.legend(loc="lower right")

if __name__ == "__main__":
    input_dir = 'input'
    # 获取 input 文件夹下所有以 .prob 结尾的文件
    prob_files = [f for f in os.listdir(input_dir) if f.endswith('.prob')]

    valid_files = []
    for prob_file in prob_files:
        base_name = os.path.splitext(prob_file)[0]
        sol_file = base_name + '.sol'
        prob_file_path = os.path.join(input_dir, prob_file)
        sol_file_path = os.path.join(input_dir, sol_file)

        # 检查对应的 .sol 文件是否存在
        if os.path.exists(sol_file_path):
            valid_files.append((prob_file_path, sol_file_path, base_name))
        else:
            print(f"对应的 .sol 文件 {sol_file} 不存在，跳过 {prob_file}。")

    num_plots = len(valid_files)
    if num_plots > 0:
        fig, axes = plt.subplots(1, num_plots, figsize=(num_plots * 5, 5))

        if num_plots == 1:
            axes = [axes]

        for i, (prob_file_path, sol_file_path, base_name) in enumerate(valid_files):
            # 加载文件
            indices, probs = load_prob_file(prob_file_path)
            positive_indices = load_sol_file(sol_file_path)

            # 生成真实标签
            true_labels = get_true_labels(indices, positive_indices)

            # 绘制ROC图并计算AUC
            plot_roc_curve(axes[i], true_labels, probs, base_name)

        plt.tight_layout()
        plt.show()