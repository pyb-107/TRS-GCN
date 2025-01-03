import matplotlib.pyplot as plt


# 历年的航班计划数量和生成的航班环数量随时间变化图
# Data for the first dataset
years = [
    '2011H1', '2011H2', '2012H1', '2012H2', '2013H1', '2013H2', '2014H1', '2014H2',
    '2015H1', '2015H2', '2016H1', '2016H2', '2017H1', '2017H2', '2018H1', '2018H2',
    '2019H1', '2019H2', '2020H1', '2020H2', '2021H1', '2021H2'
]

data1 = [
    3085, 3263, 3119, 5159, 5461, 5427, 5557, 5586, 5833, 5566, 5871, 5618, 5868, 5575,
    5752, 5806, 5853, 5723, 6913, 7113, 7720, 8120
]

# Data for the second dataset
data2 = [
    1623, 2203, 2077, 12496, 16387, 29513, 13668, 12883, 14021, 11441, 13470, 10904,
    14833, 10571, 7386, 8901, 9777, 9273, 13955, 16492, 11984, 18904
]

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(years, data1, label="flight_num", marker='o')
plt.plot(years, data2, label="paring_num", marker='x')

# Adding titles and labels
plt.title('The change of the number of national flight plans and the corresponding number of flight task rings')
plt.xlabel('Year')
plt.ylabel('Num')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
