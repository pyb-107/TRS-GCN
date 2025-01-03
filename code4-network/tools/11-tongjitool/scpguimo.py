import gurobipy as gp
import os

# 统计每个SCP问题（将lp文件放到inputdata目录下）的数据规模和变量数量等等的参数

# 设置inputdata文件夹路径
inputdata_directory = "./inputdata"

# 获取目录下所有 .lp 文件
lp_files = [f for f in os.listdir(inputdata_directory) if f.endswith('.lp')]

# 遍历每个 .lp 文件，统计变量数量、约束数量以及密度
for lp_file in lp_files:
    lp_file_path = os.path.join(inputdata_directory, lp_file)
    print(f"正在处理文件: {lp_file_path}")

    # 从 .lp 文件中读取模型
    model = gp.read(lp_file_path)

    # 获取变量数量
    num_vars = model.NumVars
    print(f"Quantity of variables (决策变量的个数): {num_vars}")

    # 获取约束数量
    num_constraints = model.NumConstrs
    print(f"Constraint quantity (约束的个数): {num_constraints}")

    # 计算覆盖矩阵的密度（非零元素比例）
    # 遍历所有约束，统计非零系数数量
    non_zero_elements = 0
    total_elements = num_vars * num_constraints  # 覆盖矩阵的总元素数

    for constr in model.getConstrs():
        row = model.getRow(constr)
        non_zero_elements += row.size()

    # 计算密度
    density = non_zero_elements / total_elements if total_elements > 0 else 0
    print(f"Density (密度): {density:.4f}")

    print("-------------------------")

print("所有文件统计完成。")
