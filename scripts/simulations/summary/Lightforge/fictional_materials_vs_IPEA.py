import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
from matplotlib import cm

# Set up paths
input_dir = '../../../../simulations/summary/Lightforge/fictional_materials'  # Directory where CSV files are located
actual_data_file = '../../../../simulations/summary/Lightforge/ionization_ip_ea.csv'  # File with actual data points
output_dir = '../../../../simulations/summary/Lightforge/fictional_materials'  # Directory to save the plots
os.makedirs(output_dir, exist_ok=True)

# Load all CSV files from the input directory
csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

# Create a list to hold dataframes and corresponding material names
dataframes = []
material_names = []

# Read each CSV file and store the dataframe and corresponding material name (without .csv)
for file in csv_files:
    df = pd.read_csv(os.path.join(input_dir, file))
    material_name = file.replace('.csv', '')  # Remove .csv extension
    dataframes.append(df)
    material_names.append(material_name)

# Calculate IP - EA difference for each dataset
for df in dataframes:
    df['IP_EA_diff'] = df['IP'] - df['EA']
    df.sort_values(by='IP_EA_diff', inplace=True)  # Sort data based on IP - EA difference

# Read the actual data
actual_data = pd.read_csv(actual_data_file)

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
colors = cm.get_cmap('Set1', len(dataframes))  # Get a color palette with distinct colors for each dataset

# Plot each dataset with lines and keep track of unique materials for the legend
for i, df in enumerate(dataframes):
    material_label = material_names[i]
    # Plot the lines for the material (sorted data)
    ax.plot(df['IP_EA_diff'], df['ionization'], color=colors(i), label=material_label, linestyle='-', marker='')

# Add actual data points for matching materials and ensure only one legend entry
for i, material in enumerate(material_names):
    matching_row = actual_data[actual_data['material'] == material]
    if not matching_row.empty:
        # Only add the actual data points, reusing the color of the corresponding line
        ax.scatter(matching_row['IP'] - matching_row['EA'], matching_row['efficiency'], color=colors(i), label=None, marker='o', s=50)

# Add labels and title
ax.set_xlabel('IP - EA Difference [eV]')
ax.set_ylabel('Ionization')
ax.set_title('Ionization vs IP - EA Difference')

# Add a legend for all datasets (only the line, no repeated points)
handles, labels = ax.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))  # Remove duplicate labels
ax.legend(unique_labels.values(), unique_labels.keys(), loc='best')

# Adjust the layout to make everything fit nicely
plt.tight_layout()

plt.ylim([0.0, 1.0])

# Save the plot as both PNG and PDF
plot_png = os.path.join(output_dir, 'ionization_vs_ip_ea_with_actual_sorted.png')
plot_pdf = os.path.join(output_dir, 'ionization_vs_ip_ea_with_actual_sorted.pdf')

plt.savefig(plot_png, dpi=300)  # Save as PNG
plt.savefig(plot_pdf)           # Save as PDF

# Show the plot
plt.show()
