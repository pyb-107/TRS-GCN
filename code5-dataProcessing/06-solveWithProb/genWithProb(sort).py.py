import gurobipy as gp
from gurobipy import GRB
import os


# 从 0.lp 文件中读取目标函数系数和约束条件
def read_lp_file():
    obj_coeffs = {}
    constraints = []
    rhs = []
    binary_vars = []
    file_path = os.path.join('input', '0.lp')
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # 读取目标函数系数
        objective_line = [line for line in lines if line.startswith('OBJ:')][0]
        parts = objective_line.split('+')[1:]
        for part in parts:
            parts2 = part.strip().split(' ')
            var_name = parts2[1]
            var_index = int(var_name[1:]) - 1
            coeff = float(parts2[0])
            obj_coeffs[var_index] = coeff

        # 读取约束条件
        constraint_lines = [line for line in lines if line.startswith('C')]
        for line in constraint_lines:
            parts = line.split('+')[1:]
            constraint = [0] * len(obj_coeffs)
            for part in parts:
                parts2 = part.strip().split(' ')
                var_name = parts2[1]
                var_index = int(var_name[1:]) - 1
                constraint[var_index] = 1
            constraints.append(constraint)
            rhs.append(1)

        # 读取二进制变量
        binary_line = [line for line in lines if line.startswith('binary')][0]
        vars = binary_line.split(' ')[1:]
        for var in vars:
            var_index = int(var[1:]) - 1
            binary_vars.append(var_index)

    return list(obj_coeffs.values()), constraints, rhs, binary_vars


# 从 sample_0.prob 文件中读取概率
def read_prob_file():
    max_index = 0
    file_path = os.path.join('input','sample_0.prob')
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split(' ')
            var_index = int(parts[0])
            max_index = max(max_index, var_index)
    probabilities = [0] * max_index
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split(' ')
            var_index = int(parts[0]) - 1
            probabilities[var_index] = float(parts[1])
    return probabilities


# 读取文件数据
obj_coeffs, constraints, rhs, binary_vars = read_lp_file()
probabilities = read_prob_file()

# 根据概率对变量进行排序，优先处理概率接近 0 或 1 的变量
sorted_indices = sorted(range(len(probabilities)), key=lambda i: min(probabilities[i], 1 - probabilities[i]))

# 创建模型
model = gp.Model("ILP")

# 设置日志文件路径
log_file_path = "sort_solve.log"
model.setParam('LogFile', log_file_path)

# 定义变量
x = {}
for i in sorted_indices:
    x[i] = model.addVar(vtype=GRB.BINARY, name=f"x{i + 1}")

# 设置目标函数
obj = gp.quicksum(obj_coeffs[i] * x[i] for i in sorted_indices)
model.setObjective(obj, GRB.MINIMIZE)

# 添加约束条件
for j in range(len(constraints)):
    constr = gp.quicksum(constraints[j][i] * x[i] for i in sorted_indices)
    model.addConstr(constr >= rhs[j], f"C{j + 1}")

# 求解模型
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    print("最优解：")
    for i in sorted_indices:
        print(f"{x[i].varName}: {x[i].x}")
    print(f"目标函数值: {model.objVal}")
else:
    print("未找到最优解")

print(f"求解日志已保存到 {log_file_path}")