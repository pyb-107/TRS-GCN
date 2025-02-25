import gurobipy as gp
from gurobipy import GRB
import os

# 定义输入文件夹路径
input_folder = 'input'

# 查找 .lp 文件和 .prob 文件
lp_files = [f for f in os.listdir(input_folder) if f.endswith('.lp')]
prob_files = [f for f in os.listdir(input_folder) if f.endswith('.prob')]

if not lp_files or not prob_files:
    print("未找到 .lp 或 .prob 文件，请检查 input 文件夹。")
else:
    lp_file = os.path.join(input_folder, lp_files[0])
    prob_file = os.path.join(input_folder, prob_files[0])

    # 读取预测概率文件
    probabilities = []
    with open(prob_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    prob = float(parts[1])
                    probabilities.append(prob)
                except ValueError:
                    print(f"无法将 {parts[1]} 转换为浮点数，请检查 .prob 文件内容。")
                    break
            else:
                print("文件格式错误，请确保每行至少包含变量编号和概率值两部分。")
                break

    if probabilities:
        # 设定阈值，这里是 10%
        threshold = 0.1
        num_vars = len(probabilities)
        num_to_remove = int(num_vars * threshold)

        # 获取概率最小的变量索引
        sorted_indices = sorted(range(num_vars), key=lambda i: probabilities[i])
        indices_to_remove = sorted_indices[:num_to_remove]

        model_original = gp.read(lp_file)
           # 获取变量列表
        vars_list = model_original.getVars()
        for index in indices_to_remove:
            var = vars_list[index]
            var.lb = 0
            var.ub = 0

        # 缩小问题后求解
        print("开始求解缩小规模后的问题...")
        reduced_log_file = 'reduced_solve.log'
        model_original.setParam('LogFile', reduced_log_file)
        model_original.setParam('TimeLimit', 200)  # 设置时间限制为 60 秒
        model_original.optimize()

        print(f"缩小规模后问题求解日志已保存到 {reduced_log_file}")