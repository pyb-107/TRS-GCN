# -*- coding: utf-8 -*-
"""
@author
"""

from gurobipy import *
import read_csv

str_path = 'input'
lt_p, dt_p = read_csv.get_pairings(str_path)
lt_f, dt_f = read_csv.get_flight(str_path)
lt_c, dt_cost_p = read_csv.compute_costs_eachpairing(str_path)

lt_delta_fp = read_csv.compute_delta_flight_per_pairing(str_path)

p = len(lt_p)  # 此为pairing的数量
f = len(lt_f)  # 此为flight的数量
F = [i for i in range(f)]
P = [j for j in range(p)]

main_prob_relax = Model()

# 添加变量
Xp = main_prob_relax.addVars(p, obj=lt_c[:p], lb=0, vtype=GRB.BINARY, name='x')

# 添加约束
column_index = main_prob_relax.addConstrs(sum(lt_delta_fp[i][j] * Xp[j] for j in P) == 1 for i in F)

# 添加约束
main_prob_relax.optimize()


# 自定义LP文件生成
def generate_custom_lp(model, filename, lt_c, lt_delta_fp):
    """
    Generate a custom LP file format for the given model.
    """
    with open(filename, 'w') as lp_file:
        # Objective function
        lp_file.write("minimize\nOBJ:" + "".join([f" + {lt_c[j]} x{j + 1}" for j in range(len(lt_c))]) + "\n")

        # Constraints
        lp_file.write("\nsubject to\n")
        count = 1
        for i in range(len(lt_delta_fp)):
            constraint = " + ".join(
                [f"{lt_delta_fp[i][j]} x{j + 1}" for j in range(len(lt_delta_fp[i])) if lt_delta_fp[i][j] != 0])
            lp_file.write(f"C{count}: {constraint} = 1\n")
            count += 1

        # Binary variables
        lp_file.write("\nbinary\n" + " ".join([f"x{j + 1}" for j in range(len(lt_c))]) + "\n")


# Generate and save the custom LP file
generate_custom_lp(main_prob_relax, 'output/0.lp', lt_c, lt_delta_fp)

# 将输出结果保存到文件中，包括目标值
output_file_path = 'output/solution.txt'  # 保存结果的文件路径
with open(output_file_path, 'w') as output_file:
    # 保存优化目标值
    output_file.write(f'Objective Value: {main_prob_relax.ObjVal}\n')

    # 保存变量及其对应的值
    for v in main_prob_relax.getVars():
        if v.X != 0.0:
            output_file.write(f'{v.VarName} {v.X}\n')

print(f'Results, including the objective value, have been saved to {output_file_path}')
