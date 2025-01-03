import matplotlib.pyplot as plt

# Data for the first model
epochs_1 = [i for i in range(0, 191, 10)]
loss_1 = [2.1597, 0.4597, 0.2352, 0.1305, 0.1280, 0.1259, 0.1246, 0.1237, 0.1231, 0.1223, 0.1220, 0.1216, 0.1213, 0.1210, 0.1208, 0.1208, 0.1205, 0.1204, 0.1202, 0.1202, 0.1202]

# Data for the second model
epochs_2 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
loss_2 = [0.73263610899448395, 0.30501282811164856, 0.20956651866436005, 0.21984723210334778, 0.22628532350063324, 0.21269989013671875,
          0.21280831098556519, 0.2284678965806961, 0.2256929725408554, 0.2014976143836975, 0.2234528362751007, 0.23225827515125275,
          0.21681052446365356, 0.2119912952184677, 0.22816511988639832, 0.21545088291168213, 0.21592743694782257,
          0.2244366705417633, 0.2405872344970703, 0.2183505743741989]

# Adjusting the data length to match
epochs_1 = epochs_1[:20]
loss_1 = loss_1[:20]

# Plotting the loss over epochs for both models
plt.figure(figsize=(10, 6))
plt.plot(epochs_1, loss_1, label='TRS-GCN', marker='o')
plt.plot(epochs_2, loss_2, label='Bartunov\'s Model', marker='x')

# Labels and title
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Loss Progression for Two Models')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
