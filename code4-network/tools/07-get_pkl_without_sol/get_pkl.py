import os
import sys
import os
sys.path.append( f'{os.path.dirname(os.path.realpath(__file__))}/../')

import argparse
import multiprocessing as mp
import pickle
import glob
import numpy as np
import shutil
import gzip
from os.path import expanduser
import pyscipopt as scip
import utils

# 这个函数的作用是将线性规划问题（输入lp文件）提取特征（转化为PKL文件）然后以供模型做预测

def read_sol_file(filepath):
    sol = set()
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            var_name = line.strip()
            sol.add(var_name)
            sol.add(f't_x{var_name}')
    return sol



class SamplingAgent(scip.Branchrule):

    def __init__(self, sol, write_to):
        self.sol = sol
        self.write_to = write_to


    def branchexeclp(self, allowaddcons):

        if self.model.getNNodes() == 1:
            ys = []
            cands = []
            cands_dict = self.model.getMapping()
            name_index_mapping = {}

            for lp_col_idx, name in cands_dict.items():
                cands.append(lp_col_idx)
                if name in self.sol:
                    ys.append(lp_col_idx)
                name_index_mapping[name] = lp_col_idx

            state_ding, obj_coef_idx = utils.extract_ding_variable_features(self.model)
            data = [state_ding, ys, cands, obj_coef_idx]

            with gzip.open(self.write_to, 'wb') as f:
                pickle.dump({
                    'data': data,
                    'mapping': name_index_mapping,
                    }, f)
            print(f'write {self.write_to}\n')
            # end the scip solving process
            self.model.interruptSolve()
        else:
            self.model.interruptSolve()

        # result = self.model.executeBranchRule('relpscost', False)
        return {"result": scip.SCIP_RESULT.DIDNOTRUN}

def collect_samples(data_dir):
    require_sol = 'eval' not in data_dir and 'time' not in data_dir
    require_sol = False

    def collect_single(id, sol_path=None):
        sample_file = os.path.join(data_dir, f'sample_{id}.pkl')
        if os.path.exists(sample_file):
            print(f"skipping {sample_file}")
            sys.stdout.flush()
            return

        m = scip.Model()
        m.setIntParam('display/verblevel', 0)
        problem = os.path.join(data_dir, f'{id}.lp')
        if not os.path.exists(problem):
            # print(f"Problem file {problem} does not exist. Skipping...")
            return
        m.readProblem(problem)

        utils.init_scip_params(m, presolving=False, seed=0)

        # 禁用预处理、启发式和分离
        m.setIntParam('presolving/maxrounds', 0)
        m.setHeuristics(scip.SCIP_PARAMSETTING.OFF)
        m.setSeparating(scip.SCIP_PARAMSETTING.OFF)

        print(f"begin collect {os.path.join(data_dir, f'sample_{id}.pkl')}")
        sys.stdout.flush()

        branchrule = SamplingAgent(
            sol=read_sol_file(sol_path) if require_sol else set(),
            write_to=os.path.join(data_dir, f'sample_{id}.pkl'))

        m.includeBranchrule(
            branchrule=branchrule,
            name="Sampling branching rule", desc="",
            priority=9999999, maxdepth=0, maxbounddist=1)
        # m.setIntParam('presolving/maxrounds', 0)  # 禁用预处理
        # m.setSeparating(scip.SCIP_PARAMSETTING.OFF)  # 禁用分离
        # m.setIntParam('lp/solvefreq', -1)  # 强制每次进入分支前重新求解LP

        m.optimize()

        # Check optimization status and print result
        status = m.getStatus()
        print(status)

        m.freeProb()

    if require_sol:  # construct training and test data, must have .sol for each .lp
        ids = []
        sols = []
        for i in range(0, 3000):
            sol_filepath = os.path.join(data_dir, f'{i}.sol')
            if os.path.exists(sol_filepath):
                ids.append(i)
                sols.append(sol_filepath)

        for cur_id, cur_sol_path in zip(ids, sols):
            collect_single(cur_id, cur_sol_path)
    else:  # construct training and test data, for all .lp files
        for i in range(0, 3000):
            collect_single(i, None)

def remove_broken_sample(data_dir):

    for i in range(0, 3000):
        sample_file = os.path.join(data_dir, f'sample_{i}.pkl')
        if os.path.exists(sample_file):
            try:
                with gzip.open(sample_file, 'rb') as f:
                    sample = pickle.load(f)
            except:
                print(f'<{sample_file}> is broken. removing...')
                os.remove(sample_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    home = expanduser("~")
    # data_dir = f'{home}/storage1/instances/scp/test'
    data_dir = os.path.join(os.getcwd(), 'data')
    remove_broken_sample(data_dir)
    collect_samples(data_dir)

