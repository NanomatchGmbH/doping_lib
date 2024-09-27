import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
from matplotlib import cm

# Load the data from two CSV files

# todo read here all csv files which are in ../../../../simulations/summary/Lightforge/fictional_materials
# df1 = pd.read_csv('../../../../simulations/summary/Lightforge/fictional_materials')
# df2 = pd.read_csv('path_to_your_second_csv_file.csv')

# todo df1, df2 --> make automatic df[0] etc.

# todo: names of those csv files are names of materials!!! of course .csv must be ignored.

# Compute the IP - EA difference for both datasets
df1['IP_EA_diff'] = df1['IP'] - df1['EA']
df2['IP_EA_diff'] = df2['IP'] - df2['EA']

# Set up directory to save the plots
output_dir = './plots'
os.makedirs(output_dir, exist_ok=True)

# Plot settings for Advanced Materials journal style
mpl.rcParams['font.family'] = ['Arial', 'Helvetica', 'sans-serif']
half_page_width = 7.08 / 2  # Half of a full-page width (7.08 inches for full width)
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
mpl.rcParams['legend.fontsize'] = 7

# Create the figure
fig, ax = plt.subplots(figsize=(half_page_width, 4.5))  # Half-page width and height adjustment

# Use a vibrant color palette (Set1) or another scientific palette (like cmocean)
colors = cm.get_cmap('Set1', 8)  # Get a palette with 8 distinct colors from Set1

# Plot the first dataset
ax.scatter(df1['IP_EA_diff'], df1['ionization'], color=colors(0), label='Dataset 1: Ionization vs IP-EA')  # todo: labels: please use labels as the names of the corresponding csv files! wuithout csv of course. make automatically

# Plot the second dataset
ax.scatter(df2['IP_EA_diff'], df2['ionization'], color=colors(1), label='Dataset 2: Ionization vs IP-EA')

# Add labels and title
ax.set_xlabel('IP - EA Difference [eV]')
ax.set_ylabel('Ionization')
ax.set_title('Ionization vs IP - EA Difference')

# Add a legend for both datasets
ax.legend()

# Adjust the layout to make everything fit nicely
plt.tight_layout()

# Save the plot as both PNG and PDF
plot_png = os.path.join(output_dir, 'ionization_vs_ip_ea.png')
plot_pdf = os.path.join(output_dir, 'ionization_vs_ip_ea.pdf')

plt.savefig(plot_png, dpi=300)  # Save as PNG
plt.savefig(plot_pdf)           # Save as PDF

# Show the plot
plt.show()
