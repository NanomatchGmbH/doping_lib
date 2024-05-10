import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Load data from a CSV file
data = pd.read_csv("all_simulations_conductivity.csv")  # Ensure you have the correct file path here

# Calculate standard error from standard deviation (sigma_std)
data['std_err'] = np.sqrt(data['sigma_std [S/cm]'])
data['IP - EA [eV]'] = 4.0 - data['simulation']


# Set up the plotting environment
sns.set(style="whitegrid")

# Create the plot with log scale for the y-axis
plt.figure(figsize=(10, 6))
plot = sns.lineplot(x='IP - EA [eV]', y='sigma [S/cm]', data=data, marker='o')

# Adding error bars
# plt.errorbar(data['IP - EA [eV]'], data['sigma [S/cm]'], data['std_err'], fmt='o', capsize=5)

# Set the y-axis to logarithmic scale
plt.yscale('log')

# Set the y-axis limit to span from the maximum value down by no more than 5 orders of magnitude
max_value = data['sigma [S/cm]'].max()
plt.ylim(max_value / 1e5, max_value * 1.1)

# Adding labels and title
plt.xlabel('IP - EA [eV]')
plt.ylabel('Conductivity (S/cm)')
plt.title('Conductivity vs IP-EA [eV]')

# Show the plot
plt.show()

