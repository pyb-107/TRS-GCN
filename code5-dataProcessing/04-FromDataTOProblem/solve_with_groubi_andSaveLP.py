from gurobipy import *
import read_csv
import csv
import os
import datetime
import math
import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    return encoding
def get_flight(str_path):
    '''
    读取所有的航班
    :return:航班号列表
    :return:字典{key=航班号,value=[出发地,目的地,持续时间]}
    '''
    path = str_path + r'\preDeal_2011.3.27-2011.10.28.csv'

    # 读取航班文件
    if os.path.exists(path):
        reader = csv.reader(open(path, 'r',encoding="utf-8"))

    reader = list(reader)
    # lt_flight_no 列表,flight No.
    lt_flight_no = []
    # result字典,key = flight No., value=[Origin,Destination,last_hour]
    result = {}

    for row in reader[1:]:
        # 计算每个航班在空中持续的时间(秒) flight time
        last_sec = (datetime.datetime.strptime(
            row[5], '%H:%M:%S') - datetime.datetime.strptime(row[4], '%H:%M:%S')).total_seconds()
        # 根据Additional Information 2 计算duty duration, 其中brief period = 15min, 时间来自input文件夹中的txt文件.
        # duty duration = flight time + 2 * brief period
        last_hour = math.ceil((last_sec/60 + 15*2)/60)
        # 将航班结果存入result字典,key = flight No., value=[Origin,Destination,last_hour]
        result[row[0]] = [row[1], row[2], last_hour]
        # 将flight No. 存入flight list
        lt_flight_no.append(row[0])
    # 该函数的返回值
    return lt_flight_no,result


def get_pairings(str_path):
    '''
    读取所有的航班串
    :return:航班串编号（从1一直到两万多）
    :return:字典{key=航班串编号,value=[航班1、航班2...]}
    '''
    path = str_path + r'\paring_2011.3.27-2011.10.28.csv'

    if os.path.exists(path):
        read = csv.reader(open(path, 'r'))

    reader = list(read)
    # result字典,key = pairing No., value=[flight1,flight2,...]
    result = {}
    # lt_pairing_no列表,存放pairing No
    lt_pairing_no = []
    for r in reader[1:]:
        # 字符串处理
        str_pair = r[1][1:-1]
        str_pair = str_pair.replace('\'', '')
        str_pair = str_pair.replace(' ', '')
        lt_flight = str_pair.split(',')
        # result字典,key = pairing No., value=[flight1,flight2,...]
        result[int(r[0])] = lt_flight
        # 存放pairing No
        lt_pairing_no.append(int(r[0]))
    return lt_pairing_no,result




def compute_costs_eachpairing(str_path):
    '''
    :return: 字典{key=航班串编号,value=总开支}
    '''
    lt_pairing,dt_pairing = get_pairings(str_path)
    lt_flight,dt_flight = get_flight(str_path)
    # dt_hotel_cost = get_city_hotel_cost(str_path)

    # 字典形式存储所有pairing的cost
    result = {}

    for k, v in dt_pairing.items():
        # 计算每个pairing的costs
        # 首先判断有没有回到起点城市
        hotel_cost = 0
        # if dt_flight[v[0]][0] == dt_flight[v[-1]][1]:
        #     # 如果回来了,就不过夜
        #     hotel_cost = 0
        # else:
        #     # 如果没回来,就需要过夜
        #     # 过夜成本的计算就是计算一天在飞机所在地的飞行成本
        #     hotel_cost = dt_hotel_cost[dt_flight[v[-1]][1]]
        # 计算单个航班串的飞行总时间
        flight_hour = sum(dt_flight[f][2] for f in v)
        # 计算飞机飞行成本
        flight_cost = flight_hour * (120 + 55 + 18 * 2)
        # 计算固定成本计算
        fixed_cost = 98 + 35 + 15 * 2
        # 将总成本存储到字典中
        result[k] = fixed_cost + flight_cost + hotel_cost
    # 列表形式存储pairing的cost
    lt_cost = []
    for p in lt_pairing:
        lt_cost.append(result[p])
    return lt_cost, result


# 生成航班串矩阵其中列表示航班串编号，行表示每一趟航班
def compute_delta_flight_per_pairing(str_path):
    lt_pairing, dt_pairing = get_pairings(str_path)
    lt_flight, dt_flight = get_flight(str_path)
    # 获取所有△pf 的01矩阵
    result = [[1 if f_k in dt_pairing[p_k] else 0 for p_k in lt_pairing] for f_k in lt_flight]
    return result

str_path = 'input'
lt_p, dt_p = get_pairings(str_path)
lt_f, dt_f = get_flight(str_path)
lt_c, dt_cost_p = compute_costs_eachpairing(str_path)

lt_delta_fp = compute_delta_flight_per_pairing(str_path)

p = len(lt_p)  # 此为pairing的数量
f = len(lt_f)  # 此为flight的数量
F = [i for i in range(f)]
P = [j for j in range(p)]

main_prob_relax = Model()  # 松弛后的列生成主问题, xp被松弛为正实数, 只有连续模型才可以求得对偶变量Pi

# 构造主问题模型, 选择的初始pairing选择方案, 1 flight = 1 pairing

# 添加变量
Xp = main_prob_relax.addVars(p, obj=lt_c[:p], lb=0, vtype=GRB.BINARY, name='x')

# 添加约束
column_index = main_prob_relax.addConstrs(sum(lt_delta_fp[i][j] * Xp[j] for j in P) == 1 for i in F)




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
            lp_file.write(f"C{count}: {constraint} >= 1\n")
            count += 1

        # Binary variables
        lp_file.write("\nbinary\n" + " ".join([f"x{j + 1}" for j in range(len(lt_c))]) + "\n")


# Generate and save the custom LP file
generate_custom_lp(main_prob_relax, 'output/0.lp', lt_c, lt_delta_fp)

# # 将输出结果保存到文件中，包括目标值
# output_file_path = 'output/solution.txt'  # 保存结果的文件路径
# with open(output_file_path, 'w') as output_file:
#     # 保存优化目标值
#     output_file.write(f'Objective Value: {main_prob_relax.ObjVal}\n')
#
#     # 保存变量及其对应的值
#     for v in main_prob_relax.getVars():
#         if v.X != 0.0:
#             output_file.write(f'{v.VarName} {v.X}\n')
#
# print(f'Results, including the objective value, have been saved to {output_file_path}')
