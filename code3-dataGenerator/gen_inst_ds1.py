import sys
import os
import time
import os, sys
import argparse
import numpy as np
import scipy.sparse
import scipy.io as sio
from itertools import combinations
from os.path import expanduser
from os import path
import re
from functools import cmp_to_key
import random
from gurobipy import *
import gurobipy as gp
import time
import os
import sys

solveTime = 100

class DualOutput:
    """
    Custom class to redirect stdout to both console and a log file.
    """
    def __init__(self, log_file_path):
        self.console = sys.__stdout__  # Original stdout (console)
        self.log_file = open(log_file_path, 'w')  # Open the log file for writing
        self.is_closed = False  # Track whether the file is closed

    def write(self, message):
        if not self.is_closed:
            # Write the message to console
            self.console.write(message)
            # Write the message to the log file
            self.log_file.write(message)

    def flush(self):
        if not self.is_closed:
            # Ensure everything gets flushed to both places
            self.console.flush()
            self.log_file.flush()

    def close(self):
        if not self.is_closed:
            # Close the log file when done
            self.log_file.close()
            self.is_closed = True

class Graph:
    """
    Container for a graph.
    Parameters
    ----------
    number_of_nodes : int
        The number of nodes in the graph.
    edges : set of tuples (int, int)
        The edges of the graph, where the integers refer to the nodes.
    degrees : numpy array of integers
        The degrees of the nodes in the graph.
    neighbors : dictionary of type {int: set of ints}
        The neighbors of each node in the graph.
    """

    def __init__(self, number_of_nodes, edges, degrees, neighbors):
        self.number_of_nodes = number_of_nodes
        self.edges = edges
        self.degrees = degrees
        self.neighbors = neighbors

    def __len__(self):
        """
        The number of nodes in the graph.
        """
        return self.number_of_nodes

    @staticmethod
    def barabasi_albert(number_of_nodes, affinity, random):
        # 检查参数
        assert affinity >= 1 and affinity < number_of_nodes
        # 初始化节点，二向图，所以一开始只有两个节点
        edges = set()
        degrees = np.zeros(number_of_nodes, dtype=int)
        neighbors = {node: set() for node in range(number_of_nodes)}
        # 每一轮循环都会添加一个节点
        for new_node in range(affinity, number_of_nodes):
            # 第一个节点首先会连接前面所有的节点，（如果不这样做，后面由于设置了偏向链接度高的节点，则会导致后面节点一直连这个）
            if new_node == affinity:
                neighborhood = np.arange(new_node)
            #
            else:
            # 从这里开始就是优先链接了，概率就是这个neighbor_prob，当前节点的度除以所有节点的度
                neighbor_prob = degrees[:new_node] / (2 * len(edges))
            # 同时增加一点随机性
                neighborhood = random.choice(new_node, affinity, replace=False, p=neighbor_prob)
            for node in neighborhood:
                edges.add((node, new_node))
                degrees[node] += 1
                degrees[new_node] += 1
                neighbors[node].add(new_node)
                neighbors[new_node].add(node)

        graph = Graph(number_of_nodes, edges, degrees, neighbors)
        return graph


# 定义回调函数
# 定义回调函数
def mycallback(model, where):
    # 获取当前时间
    current_time = time.time()

    if where == gp.GRB.Callback.MIP:
        # 获取当前的最优目标值
        obj_val = model.cbGet(gp.GRB.Callback.MIP_OBJBST)

        # 如果最优目标值发生变化
        if obj_val < gp.GRB.INFINITY and obj_val != model._best_obj:
            # 更新最优值和时间
            model._best_obj = obj_val
            model._last_change_time = current_time
            print(f"当前时间: {current_time - model._start_time:.2f}秒, 最优值: {obj_val}")
            # 记录最优值变化
            model._log.append(f"Time: {current_time - model._start_time:.2f}, Objective: {obj_val}\n")

        # 如果总运行时间超过200秒，停止优化
        if current_time - model._start_time >= solveTime:
            print("总运行时间超过200秒，停止优化")
            model.terminate()

def generate_ds(graph, filename):

    # 这里的代码就是将上面生成的图结构转化成cplex格式的lp问题

    with open(filename, 'w') as lp_file:
        lp_file.write(
            "minimize\nOBJ:" +
            "".join([f" + {random.randint(500, 1000)} x{node + 1}" for node in range(len(graph))]) + "\n"
        )
        lp_file.write("\nsubject to\n")
        for count, node in enumerate(range(len(graph))):
            neighbors = graph.neighbors[node]
            cons = f"+1 x{node + 1}" + "".join([f" +1 x{j + 1}" for j in neighbors])
            lp_file.write(f"C{count + 1}: {cons} >= 1\n")
        lp_file.write("\nbinary\n" + " ".join([f"x{node + 1}" for node in range(len(graph))]) + "\n")



# 定义一个函数来将标准输出重定向到文件
def redirect_output_to_file(log_file_path):
    sys.stdout = open(log_file_path, 'w')  # 重定向到文件


def solve_single(lp_path, sol_path, time_limit):
    # 定义日志文件路径
    log_file_path = f"{lp_path[:-2]}log"  # 日志文件保存路径
    dual_output = DualOutput(log_file_path)  # 创建 DualOutput 实例来同时输出到文件和控制台

    # 重定向 stdout 到 dual_output 实例
    sys.stdout = dual_output

    print(f"正在求解文件: {lp_path}")

    model = gp.read(lp_path)

    model._best_obj = float('inf')  # 初始化为无穷大
    model._last_change_time = time.time()  # 记录最优值最后一次变化的时间
    model._log = []  # 用于存储最优值变化记录
    model._start_time = time.time()  # 记录求解的起始时间

    # 记录变量数量
    num_vars = model.NumVars
    model._log.append(f"Number of variables: {num_vars}\n")
    # 优化模型，并调用回调函数
    model.optimize(mycallback)

    # 计算总花费的求解时间
    total_time = time.time() - model._start_time
    model._log.append(f"Total solving time: {total_time} seconds\n")

    # 打印最优解
    if model.status == gp.GRB.OPTIMAL:
        print("最优解：")
        for v in model.getVars():
            print(f"{v.varName} = {v.x}")
    elif model.status == gp.GRB.INTERRUPTED:
        print("求解结束")

    directory = os.path.dirname(lp_path)
    file_name = os.path.basename(lp_path)

    # 将记录保存到txt文件中
    log_file_path = os.path.join(directory, f"solution_log_{file_name}.txt")
    with open(log_file_path, "w") as log_file:
        log_file.writelines(model._log)

    print(f'problem is solved with {round(model.runtime, 1)} seconds')
    with open(sol_path, 'w+') as f:
        # f.write('Obj: %f\n' % model.objVal)
        for v in model.getVars():
            if int(v.x) == 1 and v.varName[0] == 'x':
                f.write(f'{v.varName[1:]}\n')

    # 关闭文件输出
    dual_output.close()
# 你的其他代码
def solve_ds(lp_path, time_limit=50):
    sol_file_path = f'{lp_path[:-2]}sol'
    if os.path.exists(sol_file_path):
        print(f'{lp_path} has been processed, skipping!')
        return

    solve_single(lp_path, sol_file_path, time_limit=time_limit)
    sys.stdout.flush()

def gen_ds(data_dir, ninst, scale_lower, scale_upper=None, solve=True):
    os.makedirs(data_dir, exist_ok=True)
    affinity = 4

    for i in range(ninst):
        nnodes = scale_lower if scale_upper is None else random.randint(scale_lower, scale_upper + 1)
        graph = Graph.barabasi_albert(nnodes, affinity, np.random.RandomState(i))

        lp_path = os.path.join(data_dir, f'{i}.lp')
        generate_ds(graph, lp_path)

        if solve:
            sol_path = solve_ds(lp_path)


def run(type, lower, upper, is_solve, num):
    home = expanduser("~")
    data_dir = os.path.join(home, f'storage1/instances/ds/{type}_{lower}_{upper}')
    gen_ds(data_dir, num, lower, upper, solve=is_solve)


if __name__ == '__main__':
    # run('testData-with-solve',3000,3100,True,1)
    # run('testData-with-solve',5000,5100,True,1)
    # run('testData-with-solve',7000,7100,True,1)
    solveTime = 50
    run('bigpicdata',1000,5000,True,30)
    run('bigpicdata',5001,10000,True,30)
    solveTime = 100
    run('bigpicdata',10001,15000,True,30)
    run('bigpicdata',15001,20000,True,30)
