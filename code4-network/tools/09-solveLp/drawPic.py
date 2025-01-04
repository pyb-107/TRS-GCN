import os
import re
import matplotlib.pyplot as plt

# 根据问题变量数量和求解时间画散点图

# Initialize lists to store the x and y values for the scatter plot
num_variables_list = []
total_solving_time_list = []

# Define the regex patterns for extracting data
num_vars_pattern = re.compile(r"Number of variables:\s*(\d+)")
total_solving_time_pattern = re.compile(r"Total solving time:\s*([\d.]+)\s*seconds")

# Iterate over all txt files in the current directory
for file_name in os.listdir('./data'):
    if file_name.endswith('.txt'):
        with open('./data/'+file_name, 'r') as file:
            content = file.read()

            # Extract the number of variables
            num_vars_match = num_vars_pattern.search(content)
            if num_vars_match:
                num_variables = int(num_vars_match.group(1))
                num_variables_list.append(num_variables)

            # Extract the total solving time
            solving_time_match = total_solving_time_pattern.search(content)
            if solving_time_match:
                total_solving_time = float(solving_time_match.group(1))
                total_solving_time_list.append(total_solving_time)

# Plotting the data
plt.scatter(num_variables_list, total_solving_time_list)
plt.xlabel("Number of Variables")
plt.ylabel("Total Solving Time (seconds)")
plt.title("Scatter Plot of Total Solving Time vs Number of Variables")
plt.show()
