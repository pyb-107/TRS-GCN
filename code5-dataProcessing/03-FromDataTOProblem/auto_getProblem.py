import os
import csv
import datetime
import math
import chardet
from gurobipy import *

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    return encoding

def get_flight(file_path):
    '''
    读取单个preDeal文件中的航班信息
    :return:航班号列表
    :return:字典{key=航班号,value=[出发地,目的地,持续时间]}
    '''
    # 读取航班文件
    if os.path.exists(file_path):
        reader = csv.reader(open(file_path, 'r', encoding="utf-8"))
    reader = list(reader)
    # lt_flight_no 列表, flight No.
    lt_flight_no = []
    # result字典, key = flight No., value=[Origin,Destination,last_hour]
    result = {}

    for row in reader[1:]:
        last_sec = (datetime.datetime.strptime(
            row[5], '%H:%M:%S') - datetime.datetime.strptime(row[4], '%H:%M:%S')).total_seconds()
        last_hour = math.ceil((last_sec/60 + 15*2)/60)
        result[row[0]] = [row[1], row[2], last_hour]
        lt_flight_no.append(row[0])
    return lt_flight_no, result

def get_pairings(file_path):
    '''
    读取单个paring文件中的航班串
    :return:航班串编号
    :return:字典{key=航班串编号,value=[航班1、航班2...]}
    '''
    if os.path.exists(file_path):
        reader = csv.reader(open(file_path, 'r'))
    reader = list(reader)
    result = {}
    lt_pairing_no = []
    for r in reader[1:]:
        str_pair = r[1][1:-1].replace('\'', '').replace(' ', '')
        lt_flight = str_pair.split(',')
        result[int(r[0])] = lt_flight
        lt_pairing_no.append(int(r[0]))
    return lt_pairing_no, result

def compute_costs_eachpairing(flight_file, pairing_file):
    '''
    :return: 字典{key=航班串编号,value=总开支}
    '''
    lt_pairing, dt_pairing = get_pairings(pairing_file)
    lt_flight, dt_flight = get_flight(flight_file)

    result = {}
    for k, v in dt_pairing.items():
        hotel_cost = 0
        flight_hour = sum(dt_flight[f][2] for f in v)
        flight_cost = flight_hour * (120 + 55 + 18 * 2)
        fixed_cost = 98 + 35 + 15 * 2
        result[k] = fixed_cost + flight_cost + hotel_cost

    lt_cost = [result[p] for p in lt_pairing]
    return lt_cost, result

def compute_delta_flight_per_pairing(flight_file, pairing_file):
    '''
    生成航班串矩阵, 列表示航班串编号，行表示每一趟航班
    '''
    lt_pairing, dt_pairing = get_pairings(pairing_file)
    lt_flight, dt_flight = get_flight(flight_file)
    result = [[1 if f_k in dt_pairing[p_k] else 0 for p_k in lt_pairing] for f_k in lt_flight]
    return result

def generate_custom_lp(model, filename, lt_c, lt_delta_fp):
    '''
    生成LP文件
    '''
    with open(filename, 'w') as lp_file:
        lp_file.write("minimize\nOBJ:" + "".join([f" + {lt_c[j]} x{j + 1}" for j in range(len(lt_c))]) + "\n")
        lp_file.write("\nsubject to\n")
        count = 1
        for i in range(len(lt_delta_fp)):
            constraint = " + ".join([f"{lt_delta_fp[i][j]} x{j + 1}" for j in range(len(lt_delta_fp[i])) if lt_delta_fp[i][j] != 0])
            lp_file.write(f"C{count}: {constraint} >= 1\n")
            count += 1
        lp_file.write("\nbinary\n" + " ".join([f"x{j + 1}" for j in range(len(lt_c))]) + "\n")

def batch_process_input(input_dir, output_dir):
    '''
    批量处理input文件夹中的preDeal和paring文件，生成对应的LP文件
    '''
    # 获取input目录下所有的preDeal和paring文件
    predeal_files = [f for f in os.listdir(input_dir) if f.startswith('preDeal') and f.endswith('.csv')]
    pairing_files = [f for f in os.listdir(input_dir) if f.startswith('paring') and f.endswith('.csv')]

    for predeal_file in predeal_files:
        matching_paring_file = predeal_file.replace('preDeal', 'paring')
        if matching_paring_file in pairing_files:
            print(f'Processing: {predeal_file} and {matching_paring_file}')

            # 构造路径
            predeal_path = os.path.join(input_dir, predeal_file)
            pairing_path = os.path.join(input_dir, matching_paring_file)

            # 计算成本和△pf矩阵
            lt_c, dt_cost_p = compute_costs_eachpairing(predeal_path, pairing_path)
            lt_delta_fp = compute_delta_flight_per_pairing(predeal_path, pairing_path)

            # 创建模型
            p = len(lt_c)
            f = len(lt_delta_fp)
            F = [i for i in range(f)]
            P = [j for j in range(p)]

            main_prob_relax = Model()

            # 添加变量
            Xp = main_prob_relax.addVars(p, obj=lt_c[:p], lb=0, vtype=GRB.BINARY, name='x')

            # 添加约束
            column_index = main_prob_relax.addConstrs(sum(lt_delta_fp[i][j] * Xp[j] for j in P) == 1 for i in F)

            # 生成LP文件
            output_file = os.path.join(output_dir, f'{predeal_file[8:-4]}.lp')
            generate_custom_lp(main_prob_relax, output_file, lt_c, lt_delta_fp)
            print(f'LP file generated: {output_file}')

# 调用批量处理函数
input_dir = 'input'
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

batch_process_input(input_dir, output_dir)
