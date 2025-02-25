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
        threshold = 0.5
        num_vars = len(probabilities)

        # 原问题求解
        print("开始求解原问题...")

        # 创建模型并读取LP文件
        model_original = gp.read(lp_file)
        if model_original is None:
            print("无法读取 LP 文件，请检查文件格式。")
            exit()

        # 获取变量列表
        vars_list = model_original.getVars()

        # 方法 1：直接求解原问题（不使用初始解）
        print("开始直接求解原问题（不使用初始解）...")
        original_log_file = 'original_solve.log'
        model_original.setParam('LogFile', original_log_file)
        model_original.setParam('TimeLimit', 200)  # 设置时间限制为 60 秒
        model_original.optimize()

        # 检查是否成功求解
        if model_original.status == GRB.OPTIMAL:
            print("原问题求解成功！")
        else:
            print("原问题求解失败。")


        print(f"直接求解原问题的日志已保存到 {original_log_file}")
