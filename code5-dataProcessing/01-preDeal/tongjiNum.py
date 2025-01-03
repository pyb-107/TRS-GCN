import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Set up the font for displaying Chinese characters
# Make sure you have a font that supports Chinese, such as SimHei or SimSun
plt.rcParams['font.sans-serif'] = ['SimHei']  # Set SimHei font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Ensure that minus signs are displayed correctly

# Reading the CSV file into a DataFrame
file_path = 'inputData/2021-3.28-2021.10.30.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Counting the number of flights by Origin and Destination airports
airport_counts = pd.concat([df["Origin"], df["Destination"]]).value_counts().head(30)

# Plotting the bar chart
plt.figure(figsize=(10,6))
airport_counts.plot(kind='bar')
plt.title("Top 20 Airports by Flight Plan Count")
plt.xlabel("Airport")
plt.ylabel("Number of Flight Plans")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Show the plot
plt.show()
