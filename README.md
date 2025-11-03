
# Project Name

This project aims to accelerate the solution of the Aircraft Routing Problem (ARP) through the integration of deep learning and modern Mixed-Integer Linear Programming (MILP) solvers. The research primarily explores how deep learning techniques can speed up the solution of large, compact MILP models, validated using real-world flight data. Unlike traditional Column Generation and heuristic algorithms, this project employs an innovative two-stage Route Selection Graph Convolutional Network (TRS-GCN) to predict the importance of decision variables, guiding the MILP solver's search process.

The core idea of this method is to divide the ARP problem into two stages: first, using Graph Convolutional Networks (GCN) to rank and select flight strings based on their interdependencies, reducing the solution space; second, using a heuristic algorithm to address the constraints of connecting the selected flight strings, ensuring an effective and feasible flight scheduling solution.

Through these acceleration strategies, the project significantly improves the efficiency of solving MILP problems while maintaining optimality. The project includes several main modules, each with independent functions and tasks:

## Directory Structure

```
- code1-solveByCG: Column Generation Solver
- code2-solveByGurobi: Gurobi Baseline Solver
- code3-dataGenerator: Data Generator
- code4-network: Network Architecture Implementation and Training
- code5-dataProcessing: Data Processing and Experimental Results
- code6-paparPicture: Table Generator
- PySCIPOpt: SCIP Solver Source Code
```

## Module Descriptions

### code1-solveByCG
This module implements a Column Generation solver to optimize the Aircraft Routing Problem. It iteratively solves the relaxed master problem and adds new columns to approach the optimal solution.

- **Input:** Flight data, flight string data
- **Output:** Optimized flight scheduling solution
- **Algorithm:** Uses Gurobi as the solver and applies Column Generation for optimization.

### code2-solveByGurobi
This module implements a baseline solver using Gurobi to provide a reference solution for the Column Generation approach and compare optimization performance between different algorithms.

- **Input:** Flight data, flight string data
- **Output:** Gurobi baseline solution
- **Algorithm:** MILP problem solved using Gurobi.

### code3-dataGenerator
This module generates training datasets by randomly creating flight scheduling problems of varying scales for model training.

- **Input:** Flight information, flight string information
- **Output:** Randomly generated training data
- **Function:** Generates flight scheduling datasets of varying sizes, simulating real-world flight scheduling scenarios.

### code4-network
This module implements the network architecture and training code used for flight scheduling optimization. It applies deep learning models to predict and optimize flight scheduling solutions.

- **Input:** Flight scheduling data, historical optimization results
- **Output:** Trained neural network model
- **Function:** Uses deep neural networks to predict and optimize flight scheduling solutions.

### code5-dataProcessing
This module is responsible for processing data and generating various tables and experimental results used in the paper. It includes tasks such as data cleaning, data integration, and result visualization.

- **Input:** Flight scheduling data, experimental logs
- **Output:** Various experimental result tables
- **Function:** Generates and visualizes the results of the model, providing support for analysis in the paper.

### code6-paparPicture
This module generates tables, graphs, and visual content for the paper, aiding in the presentation of experimental results.

- **Input:** Experimental data
- **Output:** Tables and figures required for the paper
- **Function:** Automatically generates various tables and figures for the paper.

### PySCIPOpt
This module is the Python interface for the SCIP solver, used to solve integer programming problems. It has been restructured to implement feature extraction algorithms, facilitating better integration with other modules.

- **Input:** Linear programming problems
- **Output:** Optimized solutions
- **Function:** Provides basic functionality for solving integer programming problems and performs feature extraction to optimize the solving process.

---

## Installation Dependencies

1. Install Gurobi solver:
   ```bash
   pip install gurobipy
   ```

2. Install SCIP solver:
   ```bash
   pip install pyscipopt
   ```

3. Other dependencies:
   ```bash
   pip install numpy scipy matplotlib
   ```

## Usage Instructions

### Data Generation
Before using the models, generate the datasets. Run the `code3-dataGenerator` module to generate the required training data.

### Solving Optimization Problems
Use the `code1-solveByCG` and `code2-solveByGurobi` modules to solve the Aircraft Routing Problem. Please refer to the respective modules for code examples on how to run them.

## Contributions

Pull requests are welcome, and any suggestions and improvements are greatly appreciated!

## License

MIT License

---

# Requirements

## Python Code Dependencies

- Python version 3.6.9
- Cuda version 10.0 (required by TRIG-GNN)
- CMake version >= 3.15
- python3-venv (install by running `sudo apt-get install python3-venv`)
- Two virtual environments with different versions of TensorFlow (TF1 and TF2), created by running:
  ```bash
  python3 -m venv [env_name]
  ```
  Then activate the environment and install the respective dependencies:
  - For TF1: `source tf1/bin/activate` and run `pip3 install -r requirements_1.txt`
  - For TF2: `source tf2/bin/activate` and run `pip3 install -r requirements_2.txt`
- Latest pip (upgrade by running `pip3 install -U pip`)

## C++ Code Dependencies

- C++ Boost library is required, which can be downloaded [here](https://www.boost.org/users/download/).
- SCIP solver version 6.0.1 is required, available for download [here](https://www.scipopt.org/index.php#download). An academic license can be applied for [here](https://www.scipopt.org/index.php#license).
- After setup, build the C++ code with CMake to obtain the executable `CO`.

## Datasets

Datasets are available at [this link](https://drive.google.com/file/d/1HBBdwtQ1fa31inb9wVNcT-Tslu4WAeny/view?usp=sharing).

## Model Training

- To train GG-GCN, XGBoost, and LR models, activate the tf1 environment and then run the bash script:
  ```bash
  ./model_train.sh
  ```

- To train the TRIG-GCN model, activate the tf2 environment and run:
  ```bash
  ./model_train_trig_gcn.sh
  ```

## Model Testing

- To test GG-GCN, XGBoost, and LR models, activate the tf1 environment and run:
  ```bash
  ./model_test.sh
  ```

- To test the TRIG-GCN model, activate the tf2 environment and run:
  ```bash
  ./model_test_trig_gcn.sh
  ```

The testing results will be output to the `ret_model` folder. These results correspond to the results presented in Table 1 of our paper.

## Evaluation of Heuristics

Run the bash script `./model_predict.sh` to produce solution predictions for the proposed heuristic. Alternatively, you can skip this step and use the provided solution predictions in the dataset.

Then, run:
```bash
./heur_eval.sh
```
It takes several hours to obtain the results. Please note that each process should run on a single CPU. The intermediate results will be saved in the `ret_solver` folder.

Once the previous step is finished, run:
```bash
./calc_stats.sh
```
This should be run under the tf1 environment to generate the mean statistics, which will be saved in the `ret_solver` folder. These results correspond to the statistics in Table 2 and Table 3 of our paper.

## Generating Your Own Training/Test Problem Instances

To generate your own training and test instances, use the code in the `data_generator` directory. Each problem directory contains two files:

- `gen_inst_*`: generates problem instances with different parameters and/or solves the problem instances to optimality.
- `make_sample_*`: extracts features for problem instances and prepares training data.

Two Python packages are required for data generation:
- `gurobipy` (for solving training instances to optimality).
- `PySCIPOpt` (for feature extraction). Note that you need to install our version of PySCIPOpt included in this project for feature extraction.

