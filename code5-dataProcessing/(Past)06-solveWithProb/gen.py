import gurobipy as gp
from gurobipy import GRB

# 定义变量概率
probabilities = [
    0.0004840679466724396,
    0.001730355666950345,
    7.849929062331285e-08,
    1.2984868590137921e-05,
    0.5991576313972473,
    0.5765524506568909,
    0.4932725131511688,
    0.5486735701560974,
    0.0014206722844392061,
    0.0008259883034043014
]

# 设定阈值，这里是 10%
threshold = 0.3
num_vars = len(probabilities)
num_to_remove = int(num_vars * threshold)

# 获取概率最小的变量索引
sorted_indices = sorted(range(num_vars), key=lambda i: probabilities[i])
indices_to_remove = sorted_indices[:num_to_remove]

# 原始目标函数系数
obj_coeffs = [885, 617, 833, 774, 618, 535, 574, 526, 709, 717]

# 原始约束条件
constraints = [
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 1, 1, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 1, 0, 1, 0, 1, 1]
]

# 输出求解前的问题
print("求解前的问题：")
# 输出目标函数
obj_str = "minimize\nOBJ: " + " + ".join([f"{coeff} x{i+1}" for i, coeff in enumerate(obj_coeffs)])
print(obj_str)
# 输出约束条件
print("subject to")
for i, constr in enumerate(constraints):
    constr_str = f"C{i + 1}: " + " + ".join([f"{coeff} x{j+1}" for j, coeff in enumerate(constr) if coeff != 0]) + " >= 1"
    print(constr_str)

# 创建模型
m = gp.Model("ILP")

# 定义变量，排除要移除的变量
x = {}
for i in range(num_vars):
    if i not in indices_to_remove:
        x[i + 1] = m.addVar(vtype=GRB.BINARY, name=f"x{i + 1}")

# 构建新的目标函数，排除要移除的变量
new_obj = gp.quicksum(obj_coeffs[i - 1] * x[i] for i in x.keys())
m.setObjective(new_obj, GRB.MINIMIZE)

# 构建新的约束条件，排除要移除的变量
new_constraints = []
for j, constr in enumerate(constraints):
    new_constr = gp.quicksum(constr[i - 1] * x[i] for i in x.keys())
    m.addConstr(new_constr >= 1, f"C{j + 1}")
    new_constraints.append(new_constr)

# 输出缩小规模后的问题
print("\n缩小规模后的问题：")
# 输出新的目标函数
new_obj_str = "minimize\nOBJ: " + " + ".join([f"{obj_coeffs[i - 1]} x{i}" for i in x.keys()])
print(new_obj_str)
# 输出新的约束条件
print("subject to")
for i, constr in enumerate(new_constraints):
    constr_expr = str(constr)
    constr_str = f"C{i + 1}: {constr_expr} >= 1"
    print(constr_str)

# 求解模型
m.optimize()

# 输出结果
if m.status == GRB.OPTIMAL:
    print("最优解：")
    # 输出所有变量的解，包括移除的变量设为 0
    all_sol = {i + 1: 0 for i in range(num_vars)}
    for var in m.getVars():
        var_index = int(var.varName[1:])
        all_sol[var_index] = var.x
    for i in range(num_vars):
        print(f"x{i + 1}: {all_sol[i + 1]}")
    print(f"目标函数值: {m.objVal}")
else:
    print("未找到最优解")