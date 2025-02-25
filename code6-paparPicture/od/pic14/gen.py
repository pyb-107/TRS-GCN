from matplotlib import pyplot as plt

# 使用模型进行优化前后对比图
def size3000():
    # Data for Gap values and time
    time = [8.0, 10.9, 14.5, 14.6, 14.7, 17.3, 20.0, 20.7, 34.6, 45.4, 48.5, 51.6,
            63.5, 65.9, 68.4, 70.8, 73.4, 79.7, 81.1, 82.8, 96.3, 100.0, 113.2]
    gap = [44.1, 15.0, 7.01, 6.02, 4.58, 4.56, 4.47, 4.37, 4.21, 4.13, 3.97, 3.89,
           3.81, 3.76, 3.68, 3.65, 3.44, 3.33, 3.27, 3.21, 3.16, 3.15, 3.10]

    plt.figure(figsize=(10, 6))
    plt.plot(time, gap, marker='o')

    # Limiting the x-axis to 0-150 seconds
    plt.xlim(0, 120)

    # Adding labels and title
    plt.xlabel('Time (seconds)')
    plt.ylabel('Gap (%)')
    plt.title('Gap Changes with Time During Optimization')
    plt.legend()

    # Displaying the plot
    plt.show()

if __name__ == '__main__':
    size3000()
