import matplotlib.pyplot as plt
# Data for the first model
epochs_1 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190]

# Data for the second model
epochs_2 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190]


# Data for accuracy of both models
accuracy_1 = [0.7303, 0.8105, 0.9203, 0.9502, 0.9503, 0.9504, 0.9505, 0.9506, 0.9506, 0.9507, 0.9507, 0.9507, 0.9508, 0.9508, 0.9508, 0.9508, 0.9509, 0.9509, 0.9510, 0.9510, 0.9510]

accuracy_2 = [0.8514264320479222, 0.9018846869187849, 0.9224806201550387, 0.9180043383947939, 0.9093673965936739,
              0.9185918591859186, 0.918958562522919, 0.9117522274077217, 0.9165417291354323, 0.9227053140096618,
              0.9161704076958315, 0.9109947643979057, 0.9212736179146256, 0.9210675752413402, 0.9169423006247703,
              0.9205043859649122, 0.9181084198385236, 0.9183109707971586, 0.9031185031185032, 0.9197396963123644]

# Adjusting the data length to match
accuracy_1 = accuracy_1[:20]

# Plotting the accuracy over epochs for both models
plt.figure(figsize=(10, 6))
plt.plot(epochs_1, accuracy_1, label='TRS-GCN', marker='o')
plt.plot(epochs_2, accuracy_2, label='Bartunov\'s Model', marker='x')

# Labels and title
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Accuracy Progression for Two Models')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
