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

iter_num = 40  # 每轮迭代选取的列数

main_prob_relax = Model()  # 松弛后的列生成主问题, xp被松弛为正实数, 只有连续模型才可以求得对偶变量Pi

# 构造主问题模型, 选择的初始pairing选择方案, 1 flight = 1 pairing

# 添加变量
Xp = main_prob_relax.addVars(f, obj=lt_c[:f], lb=0, vtype=GRB.CONTINUOUS, name='x')

# 添加约束
column_index = main_prob_relax.addConstrs(sum(lt_delta_fp[i][j] * Xp[j] for j in F) == 1 for i in F)

# 添加约束
# main_prob_relax.update()
main_prob_relax.write('lp\\base.lp')
main_prob_relax.optimize()

'''
获取主问题求解状态
print(main_prob_relax.status)
'''

# 构造子问题模型
lt_iter_solve = {}
lt_iter_solve[92] = main_prob_relax.objval
for s in range(f, p, iter_num):
    # 获取对偶值
    lt_constrs = main_prob_relax.getConstrs()  # 获得所有的约束
    dual_solution = [c.Pi for c in lt_constrs]  # 获得对偶变量

    lt_add_column = []  # 用于存放此轮迭代中可入基的列
    for ss in range(s, min(p, s + iter_num)):
        # 计算slack
        slack = sum(lt_delta_fp[i][ss] * dual_solution[i] for i in range(f)) - lt_c[ss]
        if slack > 0:
            # 如果合格,则添加列
            lt_add_column.append(ss)
    # 根据上轮迭代,增加可入基列
    if len(lt_add_column) > 0:
        for p_new in lt_add_column:
            columnCoeff = [lt_delta_fp[i][p_new] for i in range(f)]
            column = Column(columnCoeff, main_prob_relax.getConstrs())
            main_prob_relax.addVar(obj=lt_c[p_new], vtype=GRB.CONTINUOUS, name="CG%d_%d" % (s, p_new), column=column)
    # 将迭代后模型lp文件保存
    main_prob_relax.write(f'lp\\base{s}.lp')
    # 求解加入新列的模型
    main_prob_relax.optimize()
    # 将迭代轮次和迭代后模型最优解保存
    lt_iter_solve[s + iter_num] = main_prob_relax.objval
    # if len(lt_iter_solve) >= 6:
    #      if lt_iter_solve[s - iter_num * 4] - lt_iter_solve[s + iter_num] < 0.001:
    #           break

# 将CG后的模型转为整数，并求解
for v in main_prob_relax.getVars():
    v.setAttr("VType", GRB.BINARY)
# 更新模型
main_prob_relax.update()
# 将最终模型lp文件保存
main_prob_relax.write('lp\\final.lp')
# 求解最终模型
main_prob_relax.optimize()

# 输出结果
for v in main_prob_relax.getVars():
    if v.X != 0.0:
        print('%s %g' % (v.VarName, v.X))

i = 0
for k, v in lt_iter_solve.items():
    print('iter:', i, '  pairing:', k, '  objval:', v)
    i = i + 1


