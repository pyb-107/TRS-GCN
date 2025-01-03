import matplotlib.pyplot as plt

# 使用模型进行优化前后对比图
def size3000():
    # Data for the first set of values (new request)
    time_1_new = [1.0, 2.1, 3.3, 5.7, 6.8, 7.9, 9.0, 10.0, 11.1, 12.3, 13.6, 14.8, 16.0, 22.0, 26.7, 27.8, 29.3, 30.3, 31.5, 32.6, 33.8, 35.1, 37.3, 38.6, 40.0]
    objective_1_new = [367930.0, 221414.0, 221414.0, 221094.0, 221094.0, 220983.0, 220880.0, 220378.0, 220212.0, 219809.0, 219705.0, 219446.0, 219446.0, 219446.0, 219107.0, 219107.0, 219107.0, 219107.0, 219107.0, 219107.0, 219107.0, 219070.0, 219070.0, 219070.0, 219070.0]

    # Data for the second set of values (new request)
    time_2_new = [1.3, 2.8, 4.0, 6.2, 7.3, 8.3, 9.3, 10.4, 11.5, 12.6, 14.3, 17.6, 18.7, 20.0, 23.9, 24.9, 26.5, 27.7, 28.9, 29.9, 31.1, 32.2, 35.8, 36.8, 37.8, 38.9, 40.2]
    objective_2_new = [221388.0, 220993.0, 220040.0, 219572.0, 219572.0, 219572.0, 219572.0, 219572.0, 219523.0, 219345.0, 219100.0, 218955.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0, 218953.0]
    # Plotting the new two sets of data, focusing only on 0-25 seconds
    plt.figure(figsize=(10, 6))
    plt.plot(time_1_new, objective_1_new, label='not use model', marker='o')
    plt.plot(time_2_new, objective_2_new, label='use model', marker='x')

    # Limiting the x-axis to 0-25 seconds
    plt.xlim(0, 10)

    # Adding labels and title
    plt.xlabel('Time (seconds)')
    plt.ylabel('Objective Value')
    plt.title('problem size 3000')
    plt.legend()

    # Displaying the plot
    plt.show()
def size5000():
    # Data for the first set of values (new request)
    time_1_latest = [3.2, 4.4, 5.6, 6.9, 8.1, 10.1, 11.3, 12.5, 13.6, 14.7, 15.7, 16.9, 18.0, 19.0, 20.3, 23.3, 24.6,
                     26.1, 27.1, 28.7, 29.9, 31.5, 33.8, 35.5, 36.9, 38.3, 40.0]
    objective_1_latest = [603934.0, 360383.0, 357929.0, 357828.0, 356849.0, 356405.0, 356405.0, 356405.0, 354462.0,
                          354343.0, 354343.0, 354109.0, 354014.0, 354014.0, 353631.0, 353512.0, 353378.0, 353190.0,
                          353190.0, 352966.0, 352884.0, 352884.0, 352884.0, 352813.0, 352813.0, 352813.0, 352813.0]

    # Data for the second set of values (new request)
    time_2_latest = [2.3, 5.4, 6.4, 7.8, 9.2, 10.5, 18.0, 19.2, 20.3, 21.3, 22.4, 23.7, 24.8, 26.0, 27.1, 28.2, 29.4,
                     30.7, 32.0, 35.6, 36.7, 37.8, 38.8, 40.0]
    objective_2_latest = [356500.0, 356056.0, 355817.0, 355817.0, 355817.0, 355419.0, 355379.0, 355379.0, 355379.0,
                          355379.0, 355379.0, 355379.0, 355379.0, 355379.0, 355379.0, 355251.0, 355182.0, 355052.0,
                          354911.0, 354664.0, 353921.0, 353921.0, 353921.0, 353921.0]

    # Plotting the latest two sets of data
    plt.figure(figsize=(10, 6))
    plt.plot(time_1_latest, objective_1_latest, label='First Set (Latest)', marker='o')
    plt.plot(time_2_latest, objective_2_latest, label='Second Set (Latest)', marker='x')
    # Limiting the x-axis to 0-25 seconds
    plt.xlim(0, 15)
    # Adding labels and title
    plt.xlabel('Time (seconds)')
    plt.ylabel('Objective Value')
    plt.title('Objective Value vs Time for Two Latest Data Sets')
    plt.legend()

    # Displaying the plot
    plt.show()

def size7000():
    # Data for the first set of values (latest request)
    time_1_latest_new = [8.4, 11.0, 14.6, 17.4, 20.2, 21.5, 36.0, 37.1, 38.8, 39.9, 41.6, 42.8, 44.0, 45.4, 46.4, 48.2,
                         50.0, 51.1, 53.2, 54.4, 55.4, 57.6, 60.6, 61.6, 63.7, 65.6, 66.8, 67.8, 69.2, 70.5, 71.9, 73.3,
                         74.7, 76.5, 78.5, 80.1, 81.5, 83.3, 84.9, 86.9, 88.4, 93.6]
    objective_1_latest_new = [877475.0, 514354.0, 513362.0, 512619.0, 512441.0, 511635.0, 511270.0, 511270.0, 511270.0,
                              511270.0, 511270.0, 511270.0, 511270.0, 511270.0, 511270.0, 511270.0, 511270.0, 511012.0,
                              511012.0, 511012.0, 510563.0, 510563.0, 510441.0, 510441.0, 510441.0, 510441.0, 510441.0,
                              510441.0, 510441.0, 510441.0, 510441.0, 510441.0, 510221.0, 510221.0, 510031.0, 510031.0,
                              509762.0, 509762.0, 509314.0, 509314.0, 508726.0, 508726.0]

    # Data for the second set of values (latest request)
    time_2_latest_new = [5.6, 13.8, 16.3, 19.9, 22.7, 25.0, 26.2, 40.2, 42.0, 43.6, 45.2, 47.0, 48.8, 50.1, 51.5, 52.8,
                         54.1, 55.4, 56.9, 58.2, 59.6, 61.3, 62.3, 63.4, 65.3, 67.0, 68.4, 70.4, 71.6, 72.8, 74.4, 75.9,
                         77.2, 78.5, 79.8, 81.3, 82.6, 84.3, 97.1, 98.6, 100.1, 101.6, 112.5]
    objective_2_latest_new = [510406.0, 509883.0, 509255.0, 509255.0, 509238.0, 509238.0, 509184.0, 509039.0, 509024.0,
                              509024.0, 509024.0, 509024.0, 509024.0, 509024.0, 509024.0, 509024.0, 509024.0, 509024.0,
                              509024.0, 509024.0, 509024.0, 509024.0, 509024.0, 509024.0, 509024.0, 509024.0, 508786.0,
                              508774.0, 508774.0, 508774.0, 508774.0, 508611.0, 508611.0, 508611.0, 508611.0, 508300.0,
                              508300.0, 508071.0, 507996.0, 507658.0, 507658.0, 507658.0, 507658.0]

    # Plotting the latest two sets of data
    plt.figure(figsize=(10, 6))
    plt.plot(time_1_latest_new, objective_1_latest_new, label='First Set (New)', marker='o')
    plt.plot(time_2_latest_new, objective_2_latest_new, label='Second Set (New)', marker='x')
    plt.xlim(0, 40)
    # Adding labels and title
    plt.xlabel('Time (seconds)')
    plt.ylabel('Objective Value')
    plt.title('Objective Value vs Time for Two New Data Sets')
    plt.legend()

    # Displaying the plot
    plt.show()


if __name__ == '__main__':
    # size3000()
    #
    # size5000()

    size7000()