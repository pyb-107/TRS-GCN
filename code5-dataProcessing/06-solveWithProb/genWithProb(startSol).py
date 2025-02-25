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
        # 设定阈值，这里是 0.5，表示大于0.5的概率值认为该变量值为 1，否则为 0
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



        # 方法 2：使用初始解求解原问题
        print("开始使用初始解求解原问题...")

        # 使用预测概率设置初始解
        for i, var in enumerate(vars_list):
            prob = probabilities[i]
            # 根据概率设置初始解
            if prob > threshold:
                var.start = 1  # 初始解为1
            else:
                var.start = 0  # 初始解为0

        # 更新模型，确保初始解生效
        model_original.update()

        # 设置求解参数
        initial_solution_log_file = 'initialSolution_solve.log'
        model_original.setParam('LogFile', initial_solution_log_file)
        model_original.setParam('TimeLimit', 200)  # 设置时间限制为 60 秒
        model_original.optimize()

        # 检查是否成功求解
        if model_original.status == GRB.OPTIMAL:
            print("使用初始解求解问题成功！")
        else:
            print("使用初始解求解问题失败。")
        print(f"使用初始解求解原问题的日志已保存到 {initial_solution_log_file}")
