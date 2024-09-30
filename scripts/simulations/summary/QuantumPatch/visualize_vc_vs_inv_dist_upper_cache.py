import os
import sys

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import yaml


# Check if the merged YAML file exists
yaml_file_path = '../../../../simulations/summary/QuantumPatch/merged_vc_data.yaml'

if not yaml_file_path:
    sys.exit("Does not exist ...")

# Set font and style for publication-quality figure
mpl.rcParams['font.family'] = 'Arial'  # Use Arial font
mpl.rcParams['font.size'] = 7          # Set font size to 7 pt
mpl.rcParams['axes.linewidth'] = 0.5   # Set axes line width
mpl.rcParams['pdf.fonttype'] = 42      # Ensure fonts are embedded in PDF

# Figure size in inches (1 inch = 2.54 cm)
width_cm = 8.5    # Width for half-page figure in cm
height_cm = 6.5   # Adjust height as needed
width_in = width_cm / 2.54
height_in = height_cm / 2.54

# Create figure and axis
fig, ax = plt.subplots(figsize=(width_in, height_in))

# List of folder names explicitly specified
folders = [
    'BFDPB@CN6-CP_0.26',
    'BPAPF@CN6-CP_0.26',
    'CBP@CN6-CP_0.2',
    'NPB@CN6-CP_0.26',
    'NPB@TCNQ_0.07',
    'TCTA@CN6-CP_0.26',
    'TCTA@F6TCNNQ_0.11',
    'TPD@F4TCNQ_0.07',
    'MeO-TPD@F4TCNQ_0.07',
    'm-MTDATA@F4TCNQ_0.07'
]

# Abbreviate folder names for legend labels if necessary
folder_labels = {
    'BFDPB@CN6-CP_0.26': 'BFDPB@CN6-CP',
    'BPAPF@CN6-CP_0.26': 'BPAPF@CN6-CP',
    'CBP@CN6-CP_0.2': 'CBP@CN6-CP',
    'NPB@CN6-CP_0.26': 'NPB@CN6-CP',
    'NPB@TCNQ_0.07': 'NPB@TCNQ',
    'TCTA@CN6-CP_0.26': 'TCTA@CN6-CP',
    'TCTA@F6TCNNQ_0.11': 'TCTA@F6TCNNQ',
    'TPD@F4TCNQ_0.07': 'TPD@F4TCNQ',
    'MeO-TPD@F4TCNQ_0.07': 'MeO-TPD@F4TCNQ',
    'm-MTDATA@F4TCNQ_0.07': 'm-MTDATA@F4TCNQ'
}

# Define markers, colors, and transparency (alpha)
markers = ['o', 's', '^', 'D', 'v', '>', '<', 'p', '*', 'h']
colors = ['b', 'g', 'r', 'c', 'm', 'k', 'y', 'gray', 'orange', 'purple']
alpha_value = 0.5  # Set transparency

# Ensure there are enough markers and colors
if len(markers) < len(folders):
    markers *= (len(folders) // len(markers) + 1)
if len(colors) < len(folders):
    colors *= (len(folders) // len(colors) + 1)

# Initialize lists to collect all inverse distances
all_inverse_distances = []


def save_data_to_yaml():
    # Initialize dictionary to hold all data
    merged_data = {}
    for folder in folders:
        vc_file = os.path.join(folder, 'vc_relevant.csv')
        if os.path.isfile(vc_file):
            # Read the CSV file
            data = pd.read_csv(vc_file)
            if 'dimer_comdist' in data.columns and 'VC_corrected' in data.columns:
                # Exclude zero or negative distances to avoid division by zero
                data = data[data['dimer_comdist'] > 0]
                inverse_distance = 1 / data['dimer_comdist']
                # Store the relevant data for each material
                merged_data[folder] = {
                    'inverse_distance': inverse_distance.tolist(),
                    'VC_corrected': data['VC_corrected'].tolist()
                }
            else:
                print(f"Required columns not found in {vc_file}")
        else:
            print(f"{vc_file} not found.")
    
    # Save the merged data into a single YAML file
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(merged_data, yaml_file)

    print(f"Merged data saved in {yaml_file_path}.")

def load_data_from_yaml():
    # Load the merged YAML file
    with open(yaml_file_path, 'r') as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.SafeLoader)

# Optionally, save or load data based on whether YAML file exists
if not os.path.isfile(yaml_file_path):
    print(f"{yaml_file_path} not found. Saving data to YAML.")
    save_data_to_yaml()

# Load data from YAML file
merged_data = load_data_from_yaml()

# Loop over each material in the YAML data and plot
for idx, (material, data) in enumerate(merged_data.items()):
    inverse_distance = np.array(data['inverse_distance'])
    vc_corrected = np.array(data['VC_corrected'])
    
    # Collect inverse distances for axis limits
    all_inverse_distances.extend(inverse_distance)
    
    # Plot the data with adjusted marker size and transparency
    ax.plot(
        inverse_distance,
        vc_corrected,
        marker=markers[idx],
        linestyle='',
        markersize=3,  # Reduced marker size
        color=colors[idx],
        label=folder_labels.get(material, material),
        alpha=alpha_value  # Set transparency
    )

# Customize the plot
ax.set_xlabel('Inverse Center of Mass Distance (1/Å)', fontsize=7)
ax.set_ylabel('$V_C$ (eV)', fontsize=7)
ax.tick_params(axis='both', which='major', labelsize=7)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Set x-axis limits based on the data range
inverse_distance_min = min(all_inverse_distances)
inverse_distance_max = max(all_inverse_distances)
ax.set_xlim(inverse_distance_min, inverse_distance_max)

# Create a secondary x-axis on top that shares the same scale
secax = ax.twiny()
secax.set_xlim(ax.get_xlim())
secax.set_xlabel('Distance (Å)', fontsize=7)
secax.tick_params(axis='both', which='major', labelsize=7)

# Set ticks on the secondary x-axis at positions corresponding to distances 4, 5, 6, 10, and 20 Å
distance_ticks = [4, 5, 6, 10, 20]  # Distances in Ångströms
inverse_distance_ticks = [1 / d for d in distance_ticks]

# Filter ticks to include only those within x-limits
ticks_in_range = [(inv_d, d) for inv_d, d in zip(inverse_distance_ticks, distance_ticks)
                  if inverse_distance_min <= inv_d <= inverse_distance_max]

if ticks_in_range:
    inverse_distance_ticks_filtered, distance_ticks_filtered = zip(*ticks_in_range)
    secax.set_xticks(inverse_distance_ticks_filtered)
    secax.set_xticklabels([f'{d}' for d in distance_ticks_filtered])
else:
    # If no ticks are in range, use default ticks
    secax.set_xticks([])
    print("No secondary x-axis ticks fall within the data range.")

# Adjust legend
ax.legend(
    fontsize=6,
    loc='upper right',
    frameon=False,
    handletextpad=0.3,
    borderpad=0.3,
    labelspacing=0.3
)

# Adjust layout for tightness
plt.tight_layout(pad=0.2)

# Save the figure in high-resolution PNG and PDF formats
plt.savefig('VC_vs_inverse_distance_with_secondary_xaxis.png', dpi=600, bbox_inches='tight')
plt.savefig('VC_vs_inverse_distance_with_secondary_xaxis.pdf', dpi=600, bbox_inches='tight')

# Display the plot (optional)
# plt.show()

