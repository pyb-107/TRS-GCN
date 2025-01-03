from matplotlib import pyplot as plt

# 使用模型进行优化前后对比图
def size3000():
    # Data for Incumbent values and time
    time = [8.0, 10.9, 14.5, 14.6, 14.7, 17.3, 20.0, 20.7, 34.6, 45.4, 48.5, 51.6,
            63.5, 65.9, 68.4, 70.8, 73.4, 79.7, 81.1, 82.8, 96.3, 100.0, 113.2]
    incumbent = [877475.0, 514354.0, 513362.0, 512893.0, 512619.0, 512441.0, 512309.0,
                 511635.0, 511270.0, 511255.0, 510563.0, 510441.0, 510221.0, 510115.0,
                 509762.0, 509314.0, 508726.0, 508399.0, 508094.0, 507847.0, 507775.0,
                 507663.0, 507503.0]

    plt.figure(figsize=(10, 6))
    plt.plot(time, incumbent, marker='o')

    # Limiting the x-axis to 0-150 seconds
    plt.xlim(0, 120)

    # Adding labels and title
    plt.xlabel('Time (seconds)')
    plt.ylabel('Object Value')
    plt.title('Object Value Changes with Time During Optimization')
    plt.legend()

    # Displaying the plot
    plt.show()

if __name__ == '__main__':
    size3000()
