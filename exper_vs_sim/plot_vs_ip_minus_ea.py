import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the merged data
df = pd.read_csv('merged_ionization_data.csv')

# Calculate IP - EA difference
df['IP-EA'] = df['IP'] - df['EA']

# Set up the plotting environment
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")

# Plotting simulation vs IP-EA
sns.scatterplot(data=df, x='IP-EA', y='simulation', color='blue', label='Simulation', s=100)

# Plotting experiment vs IP-EA
sns.scatterplot(data=df, x='IP-EA', y='experiment', color='red', label='Experiment', s=100)

# Annotate each point with its material name
for index, row in df.iterrows():
    plt.text(row['IP-EA'], row['simulation'], row['material_normalized'].lower(), color='blue', verticalalignment='bottom', fontsize=9)
    if pd.notna(row['experiment']):
        plt.text(row['IP-EA'], row['experiment'], row['material_normalized'].lower(), color='red', verticalalignment='top', fontsize=9)

# Labels and title
plt.xlabel('IP - EA (eV)')
plt.ylabel('Efficiency')
plt.title('Simulation and Experiment Efficiency vs IP-EA Difference')
plt.legend()

plt.savefig("doping_vs_ip_minus_ea", dpi=600)

# Show the plot
plt.show()

