import os
# 这份代码检查解是否满足问题的约束，并输出目标函数值
def read_lp_file(file_path):
    objective = {}
    constraints = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # 读取目标函数
        in_objective = False
        in_constraints = False
        for line in lines:
            line = line.strip()
            if not line:  # 跳过空行
                continue
            if line.startswith('minimize'):
                in_objective = True
                continue
            if line.startswith('subject to'):
                in_objective = False
                in_constraints = True
                continue
            if line.startswith('binary'):
                in_constraints = False
                continue
            if ':' not in line:  # 跳过没有冒号的行
                continue
            parts = line.split(':')[1].split()
            if in_objective:
                i = 0
                while i < len(parts):
                    if parts[i] == '+':
                        i += 1
                    coefficient = float(parts[i])
                    variable = parts[i + 1]
                    objective[variable] = coefficient
                    i += 2
            elif in_constraints:
                constraint = {}
                i = 0
                while i < len(parts) - 2:
                    if parts[i] == '+':
                        i += 1
                    coefficient = float(parts[i])
                    variable = parts[i + 1]
                    constraint[variable] = coefficient
                    i += 2
                operator = parts[-2]
                right_hand_side = float(parts[-1])
                constraints[line.split(':')[0].strip()] = (constraint, operator, right_hand_side)
    return objective, constraints

def read_sol_file(file_path):
    solution = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            variable_index = int(line.strip())
            variable = f'x{variable_index}'
            solution[variable] = 1
    return solution

def verify_solution(objective, constraints, solution):
    # 验证约束条件
    for constraint_name, (constraint, operator, right_hand_side) in constraints.items():
        left_hand_side = 0
        for variable, coefficient in constraint.items():
            left_hand_side += coefficient * solution.get(variable, 0)
        if operator == '>=':
            if left_hand_side < right_hand_side:
                return False
    # 计算目标函数值
    objective_value = 0
    for variable, coefficient in objective.items():
        objective_value += coefficient * solution.get(variable, 0)
    return objective_value

# 读取input文件夹下的所有文件
input_folder = 'input'
lp_files = [f for f in os.listdir(input_folder) if f.endswith('.lp')]

for lp_file in lp_files:
    lp_file_path = os.path.join(input_folder, lp_file)
    sol_file_name = lp_file.replace('.lp', '.sol')
    sol_file_path = os.path.join(input_folder, sol_file_name)

    if os.path.exists(sol_file_path):
        objective, constraints = read_lp_file(lp_file_path)
        solution = read_sol_file(sol_file_path)
        result = verify_solution(objective, constraints, solution)
        if result is not False:
            print(f"文件 {lp_file} 的解满足约束条件，目标函数值为: {result}")
        else:
            print(f"文件 {lp_file} 的解不满足约束条件。")
    else:
        print(f"未找到与 {lp_file} 对应的解文件 {sol_file_name}。")
