import matplotlib.pyplot as plt


# 历年的航班计划数量和生成的航班环数量随时间变化图
# Data for the first dataset
years = [
    '2011H1', '2011H2', '2012H1', '2012H2', '2013H1', '2013H2', '2014H1', '2014H2',
    '2015H1', '2015H2', '2016H1', '2016H2', '2017H1', '2017H2', '2018H1', '2018H2',
    '2019H1', '2019H2', '2020H1', '2020H2', '2021H1', '2021H2'
]

data1 = [
    6040, 7326, 5611, 8693, 8887, 8854, 10925, 10777, 10549, 10369, 11372, 11736, 13049, 13824, 16158, 15158, 17867,
    16867, 18150, 18750, 19997, 20003
]


# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(years, data1, marker='o')

# Adding titles and labels
plt.title('Line chart of changes in the number of scheduled flights')
plt.xlabel('Year')
plt.ylabel('Number of flights')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
