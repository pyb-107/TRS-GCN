import gurobipy as gp
import time
import os


# 定义回调函数
def mycallback(model, where):
    # 计算当前已用的时间，从求解开始算起
    elapsed_time = time.time() - model._start_time

    if where == gp.GRB.Callback.MIP:
        # 获取当前的最优目标值
        obj_val = model.cbGet(gp.GRB.Callback.MIP_OBJBST)

        # 每秒记录一次目标值
        if elapsed_time - model._last_record_time >= 1:
            if obj_val < gp.GRB.INFINITY:
                model._log.append(f"Time: {elapsed_time:.1f} seconds, Objective: {obj_val}\n")
                model._last_record_time = elapsed_time

        # 如果最优目标值发生变化
        if obj_val < gp.GRB.INFINITY and obj_val != model._best_obj:
            # 更新最优值和变化时间
            model._best_obj = obj_val
            model._last_change_time = time.time()  # 记录最优值变化的时间
            print(f"当前时间: {elapsed_time:.1f} seconds, 最优值: {obj_val}")

        # 如果超过30秒没有变化，停止优化
        if time.time() - model._last_change_time >= 30:
            print("超过30秒最优值没有变化，停止优化")
            model.terminate()


# 从 .prob 文件中读取初始解
def read_initial_solution(prob_file):
    initial_solution = {}
    with open(prob_file, 'r') as f:
        for line in f:
            var_index, prob = line.strip().split()
            var_index = int(var_index)
            prob = float(prob)
            # 概率大于0.9设为1，概率小于0.1设为0
            if prob > 0.7:
                initial_solution[var_index] = 1
            elif prob < 0.3:
                initial_solution[var_index] = 0
    return initial_solution


# 设置 .lp 文件目录
lp_directory = "./data"

# 获取目录下所有 .lp 文件
lp_files = [f for f in os.listdir(lp_directory) if f.endswith('.lp')]

# 遍历每个 .lp 文件进行求解
for lp_file in lp_files:
    lp_file_path = os.path.join(lp_directory, lp_file)

    # 查找对应的 .prob 文件（假设命名规则一致）
    prob_file_name = f"sample_{lp_file.split('.')[0]}.prob"
    prob_file_path = os.path.join(lp_directory, prob_file_name)

    if os.path.exists(prob_file_path):
        initial_solution = read_initial_solution(prob_file_path)
    else:
        print(f"未找到对应的初始解文件: {prob_file_name}，跳过初始解设定")
        initial_solution = {}

    print(f"正在求解文件: {lp_file_path}")

    # 创建模型并从 .lp 文件中读取
    model = gp.read(lp_file_path)

    # 设置初始解
    if initial_solution:
        for v in model.getVars():
            var_index = int(v.varName[1:])  # 假设变量名格式为 x1, x2, ...
            if var_index in initial_solution:
                v.start = initial_solution[var_index]

    # 设置初始值
    model._best_obj = float('inf')  # 初始化为无穷大
    model._last_change_time = time.time()  # 记录最优值最后一次变化的时间
    model._last_record_time = 0  # 初始化为0，控制每秒记录一次
    model._log = []  # 用于存储最优值变化记录
    model._start_time = time.time()  # 记录求解的起始时间

    # 记录变量数量
    num_vars = model.NumVars
    model._log.append(f"Number of variables: {num_vars}\n")

    # 优化模型，并调用回调函数
    model.optimize(mycallback)

    # 计算总花费的求解时间
    total_time = time.time() - model._start_time
    model._log.append(f"Total solving time: {total_time:.1f} seconds\n")

    # 打印最优解
    if model.status == gp.GRB.OPTIMAL:
        print("最优解：")
        for v in model.getVars():
            print(f"{v.varName} = {v.x}")
    elif model.status == gp.GRB.INTERRUPTED:
        print("求解因超过30秒无最优值变化被中止")

    # 将记录保存到txt文件中
    log_file_path = os.path.join(lp_directory, f"solution_log_{lp_file}.txt")
    with open(log_file_path, "w") as log_file:
        log_file.writelines(model._log)

        # 保存解的变量
        for v in model.getVars():
            if int(v.x) == 1 and v.varName[0] == 'x':
                log_file.write(f'{v.varName[1:]}\n')

    print(f"最优值记录已保存到 {log_file_path}")

print("所有文件求解完成。")
