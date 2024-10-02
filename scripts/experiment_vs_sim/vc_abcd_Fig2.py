import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import yaml
import os
import sys

# General Formatting for All Plots
mpl.rcParams['font.family'] = 'Arial'  # Use Arial font
mpl.rcParams['font.size'] = 7          # Set font size to 7 pt
mpl.rcParams['axes.linewidth'] = 0.5   # Set axes line width
mpl.rcParams['pdf.fonttype'] = 42      # Ensure fonts are embedded in PDF
mpl.rcParams['axes.labelsize'] = 7
mpl.rcParams['axes.titlesize'] = 7
mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['legend.fontsize'] = 6

# Figure size in inches (1 inch = 2.54 cm)
full_page_width = 7.08  # inches (18 cm)
fig_width = full_page_width  # For full width figure
fig_height = full_page_width * (3/4)  # Adjust height as needed

# Create figure and axes
# fig, axes = plt.subplots(2, 2, figsize=(fig_width, fig_height))
fig, axes = plt.subplots(2, 2, figsize=(fig_width, 6))
axes = axes.flatten()

# --- Plot a ---
# Use axes[0]

# Read data from the CSV file
df = pd.read_csv('../../simulations/summary/Deposit/first_rdf_peak.csv')

# Remove doping information by splitting at '_' and keeping the part before it
df['material_clean'] = df['material'].apply(lambda x: x.split('_')[0])

# Sort the DataFrame by 'first_rdf_peak' in ascending order
df_sorted = df.sort_values(by='first_rdf_peak')

# Plotting on axes[0]
axes[0].bar(df_sorted['material_clean'], df_sorted['first_rdf_peak'], color='skyblue', edgecolor='black')

# Customizing the plot for publication style
axes[0].set_xlabel('Material')
axes[0].set_ylabel('First RDF Peak (Å)')
axes[0].set_xticklabels(df_sorted['material_clean'], rotation=45, ha='right')
axes[0].set_ylim(4, )
axes[0].set_title('a', fontsize=10, fontweight='bold', loc='left')  # Bold label

# --- Plot b ---
# Use axes[1]

# Check if the merged YAML file exists
yaml_file_path = '../../simulations/summary/QuantumPatch/merged_vc_data.yaml'

if not os.path.isfile(yaml_file_path):
    sys.exit(f"{yaml_file_path} does not exist.")

# Load data from YAML file
with open(yaml_file_path, 'r') as yaml_file:
    merged_data = yaml.load(yaml_file, Loader=yaml.SafeLoader)

# Define materials and their labels
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

# Define markers and colors
markers = ['o', 's', '^', 'D', 'v', '>', '<', 'p', '*', 'h']
colors = plt.cm.tab10.colors  # Use built-in colormap for distinct colors
alpha_value = 0.5  # Set transparency

# Initialize lists to collect all inverse distances
all_inverse_distances = []

# Plotting on axes[1]
for idx, material in enumerate(folders):
    if material in merged_data:
        inverse_distance = np.array(merged_data[material]['inverse_distance'])
        vc_corrected = np.array(merged_data[material]['VC_corrected'])
        all_inverse_distances.extend(inverse_distance)
        axes[1].plot(
            inverse_distance,
            vc_corrected,
            marker=markers[idx],
            linestyle='',
            markersize=3,
            color=colors[idx % len(colors)],
            label=folder_labels.get(material, material),
            alpha=alpha_value
        )
    else:
        print(f"Data for {material} not found in the YAML file.")

# Customize the plot
axes[1].set_xlabel('Inverse Center of Mass Distance (1/Å)')
axes[1].set_ylabel('$V_C$ (eV)')
axes[1].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
axes[1].legend(fontsize=6, loc='upper right', frameon=False)

# Set x-axis limits based on the data range
inverse_distance_min = min(all_inverse_distances)
inverse_distance_max = max(all_inverse_distances)
axes[1].set_xlim(inverse_distance_min, inverse_distance_max)

axes[1].set_title('b', fontsize=10, fontweight='bold', loc='left')  # Bold label

##

# Create a secondary x-axis on top that shares the same scale (for direct distances)
secax = axes[1].twiny()
secax.set_xlim(axes[1].get_xlim())
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
axes[1].legend(
    fontsize=6,
    loc='upper right',
    frameon=False,
    handletextpad=0.3,
    borderpad=0.3,
    labelspacing=0.3
)

# Adjust layout for tightness
plt.tight_layout(pad=0.2)

##





# --- Plot c ---
# Use axes[2]

# Read the first_rdf_peak data
rdf_peak_df = pd.read_csv('../../simulations/summary/Deposit/first_rdf_peak.csv')
rdf_peak_df['clean_material'] = rdf_peak_df['material'].apply(lambda x: x.split('_')[0])
rdf_peak_df.set_index('material', inplace=True)

# Initialize a list to store results
results = []

# Process each material
for material in rdf_peak_df.index:
    first_rdf_peak = rdf_peak_df.loc[material, 'first_rdf_peak']
    clean_name = rdf_peak_df.loc[material, 'clean_material']

    # Use the material name to retrieve data from YAML
    if material in merged_data:
        data = pd.DataFrame({
            'dimer_comdist': merged_data[material]['inverse_distance'],
            'VC_corrected': merged_data[material]['VC_corrected']
        })
        data['dimer_comdist'] = 1 / data['dimer_comdist']  # Convert inverse distance back to distance

        # Find the VC at the closest distance to the first RDF peak
        idx_closest = (data['dimer_comdist'] - first_rdf_peak).abs().idxmin()
        vc_mean = data.loc[idx_closest, 'VC_corrected']

        # Append the result with clean material name
        results.append({
            'material': clean_name,
            'first_rdf_peak': first_rdf_peak,
            'VC_mean': vc_mean
        })
    else:
        print(f"Data for material {material} not found in the YAML file.")

# Create a DataFrame from the results
results_df = pd.DataFrame(results)
results_df.sort_values(by='VC_mean', inplace=True)

# Plotting on axes[2]
axes[2].barh(results_df['material'], results_df['VC_mean'], color='skyblue')
axes[2].set_xlabel('$V_C$ at First RDF Peak (eV)')
axes[2].set_ylabel('Material')
axes[2].set_xlim([-0.9, -0.6])
axes[2].set_title('c', fontsize=10, fontweight='bold', loc='left')  # Bold label

# --- Plot d ---
# Use axes[3]

import numpy as np

# Read the simulated data (IP, EA) and VC data from CSV file
sim_data = pd.read_csv('../../simulations/summary/Lightforge/ionization_ip_ea.csv')

# Read the VC data, which includes `VC_mean`
vc_data = pd.read_csv('../../simulations/summary/Deposit/VC_at_first_rdf_peak.csv')

# Read the experimental data
exp_data = pd.read_csv('../../experimental_data/summary/measured_efficiency.csv')

# Extract base material names from simulated data
def extract_base_material(material):
    if '@' in material:
        base_material = material.split('_')[0]
    else:
        base_material = material
    return base_material

sim_data['base_material'] = sim_data['material'].apply(extract_base_material)
vc_data['base_material'] = vc_data['material'].apply(extract_base_material)

# Prepare the experimental data
exp_data.rename(columns={'material_name': 'base_material', 'efficiency': 'efficiency_exp'}, inplace=True)

# Merge simulated data with VC data on `base_material`
sim_data = pd.merge(sim_data, vc_data[['base_material', 'VC_mean']], on='base_material', how='inner')

# Merge the simulated + VC data with experimental data
merged_data = pd.merge(sim_data, exp_data[['base_material', 'efficiency_exp']], on='base_material', how='inner')

# Compute IP - EA + VC (from simulations)
merged_data['IP_EA_VC_sim'] = merged_data['IP'] - merged_data['EA'] + merged_data['VC_mean']

# Create a mapping from numbers to materials
materials_info = [
    {'Number': 1, 'Material': 'BFDPB@CN6-CP', 'mol%': 26},
    {'Number': 2, 'Material': 'NPB@CN6-CP', 'mol%': 26},
    {'Number': 3, 'Material': 'BPAPF@CN6-CP', 'mol%': 26},
    {'Number': 4, 'Material': 'TCTA@CN6-CP', 'mol%': 26},
    {'Number': 5, 'Material': 'CBP@CN6-CP', 'mol%': 20},
    {'Number': 6, 'Material': 'MeO-TPD@F4TCNQ', 'mol%': 2},
    {'Number': 7, 'Material': 'm-MTDATA@F4TCNQ', 'mol%': 2},
    {'Number': 8, 'Material': 'TPD@F4TCNQ', 'mol%': 2},
    {'Number': 9, 'Material': 'TCTA@F6TCNNQ', 'mol%': 11},
    {'Number':10, 'Material': 'ZnPc@F4TCNQ', 'mol%': 2},
    {'Number':11, 'Material': 'ZnPc@TCNQ', 'mol%': 2}
]

# Create a mapping from material to number
material_numbers = {item['Material']: item['Number'] for item in materials_info}

# Assign numbers to the materials in merged_data
def get_material_number(base_material):
    return material_numbers.get(base_material, None)

merged_data['material_number'] = merged_data['base_material'].apply(get_material_number)

# Drop any rows where material_number is None (materials not in our list)
merged_data = merged_data.dropna(subset=['material_number'])

# Convert material_number to integer
merged_data['material_number'] = merged_data['material_number'].astype(int)

# Plotting on axes[3]

# Plot simulated doping efficiency
axes[3].scatter(merged_data['IP_EA_VC_sim'], merged_data['efficiency'], color='blue', marker='o', label='Simulated')

# Plot experimental doping efficiency
axes[3].scatter(merged_data['IP_EA_VC_sim'], merged_data['efficiency_exp'], color='red', marker='s', label='Experimental')

# Add unfilled circles for relative simulation values for materials 1-4
relative_simulation_values = {
    1: 1.0,
    2: 0.969025613,
    3: 0.921286021,
    4: 0.848504597
}
for i in range(1, 5):
    material_row = merged_data[merged_data['material_number'] == i]
    if not material_row.empty:
        axes[3].scatter(material_row['IP_EA_VC_sim'], relative_simulation_values[i], facecolors='none', edgecolors='blue', marker='o', label='Sim. (relative)' if i == 1 else "")

axes[3].set_xlabel('IP - EA + $V_C$ (eV)')
axes[3].set_ylabel(r'Ionization Fraction  $\eta_{\mathrm{exper}}$')
axes[3].set_title('d', fontsize=10, fontweight='bold', loc='left')  # Bold label

# Annotate data points with italic numbers
for i, row in merged_data.iterrows():
    axes[3].annotate(str(row['material_number']), (row['IP_EA_VC_sim'], row['efficiency']), textcoords="offset points",
                     xytext=(5, -5), fontsize=6, color='blue', fontstyle='italic')
    axes[3].annotate(str(row['material_number']), (row['IP_EA_VC_sim'], row['efficiency_exp']), textcoords="offset points",
                     xytext=(5, 5), fontsize=6, color='red', fontstyle='italic')

# --- Add the derivative line from panel b of the second script ---

# Specify the material for which you want to add the derivative line
material_name = 'TCTA@CN6-CP_0.26'  # Corresponds to material number 4

# Path to the CSV file for the material in the second script
csv_path = '../../simulations/summary/Lightforge/fictional_materials/{}.csv'.format(material_name)

if os.path.exists(csv_path):
    # Read the CSV file
    df_derivative = pd.read_csv(csv_path)

    # Compute IP - EA Difference
    df_derivative['IP_EA_diff'] = df_derivative['IP'] - df_derivative['EA']

    # Get VC_mean for the base material
    base_material = material_name.split('_')[0]
    vc_mean_row = vc_data[vc_data['base_material'] == base_material]
    if not vc_mean_row.empty:
        vc_mean = vc_mean_row['VC_mean'].values[0]
    else:
        print(f"VC_mean not found for {base_material}")
        vc_mean = 0  # Default to 0 if not found

    # Adjust IP_EA_diff by adding VC_mean to get IP - EA + VC
    df_derivative['IP_EA_VC'] = df_derivative['IP_EA_diff'] + vc_mean

    # Extract x (IP - EA + VC) and y (ionization fraction)
    x = df_derivative['IP_EA_VC'].values
    y = df_derivative['ionization'].values * 100  # Convert to percentage

    # Ensure x and y are sorted by x
    sorted_indices = np.argsort(x)
    x = x[sorted_indices]
    y = y[sorted_indices]

    # Compute the derivative d(IP - EA + VC)/dη using central difference
    def central_difference(x, y):
        dydx = np.zeros_like(y)
        dydx[1:-1] = (x[2:] - x[:-2]) / (y[2:] - y[:-2])
        dydx[0] = (x[1] - x[0]) / (y[1] - y[0])
        dydx[-1] = (x[-1] - x[-2]) / (y[-1] - y[-2])
        return dydx

    derivative = central_difference(y, x)

    # Convert derivative to kcal/mol per %
    derivative_kcal_per_percent = derivative * 23.0609  # eV to kcal/mol

    # Create secondary y-axis
    ax_secondary = axes[3].twinx()
    ax_secondary.set_ylabel('d(IP - EA + $V_C$)/d$\eta$ (kcal/mol/%)', color='grey', fontsize=7)
    ax_secondary.tick_params(axis='y', labelcolor='grey')

    # Plot the derivative line
    ax_secondary.plot(x, derivative_kcal_per_percent, color='grey', linestyle='--', label='Derivative')

    # Adjust x-limits to match axes[3]
    ax_secondary.set_xlim(axes[3].get_xlim())

    # Add the derivative line to the legend
    axes[3].legend(loc='upper left', frameon=False)
else:
    print(f"CSV file for {material_name} not found at {csv_path}")

# Adjust layout to make sure everything fits nicely
plt.tight_layout(pad=1.0)

# Save the figure in high-resolution PNG and PDF formats
plt.savefig('combined_figure.png', dpi=600, bbox_inches='tight')
plt.savefig('combined_figure.pdf', dpi=600, bbox_inches='tight')

# Display the plot
plt.show()
