import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import yaml
import os
import sys
import matplotlib.gridspec as gridspec

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
    {'Number': 10, 'Material': 'ZnPc@F4TCNQ', 'mol%': 2},
    {'Number': 11, 'Material': 'ZnPc@TCNQ', 'mol%': 2}
]

# Create a mapping from material to number
material_numbers = {item['Material']: item['Number'] for item in materials_info}

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

# Create figure and axes using GridSpec
fig = plt.figure(figsize=(fig_width, fig_height))
gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1.2])

# Left column
ax0 = plt.subplot(gs[0, 0])  # Top left plot (new Figure a, old Figure b)
ax1 = plt.subplot(gs[1, 0])  # Bottom left plot (combined plot with two y-axes)

# Right column (spans both rows)
ax2 = plt.subplot(gs[:, 1])  # Right plot (new Figure c, old Figure d)

# Add labels "a", "b", "c" to each subplot
ax0.text(-0.15, 1.05, "a", transform=ax0.transAxes, fontsize=12, fontweight='bold')
ax1.text(-0.15, 1.05, "b", transform=ax1.transAxes, fontsize=12, fontweight='bold')
ax2.text(-0.05, 1.05, "c", transform=ax2.transAxes, fontsize=12, fontweight='bold')

# --- Plot a (old Figure b) ---
# Use ax0

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

# Plotting on ax0
for idx, material in enumerate(folders):
    if material in merged_data:
        inverse_distance = np.array(merged_data[material]['inverse_distance'])
        vc_corrected = np.array(merged_data[material]['VC_corrected'])
        all_inverse_distances.extend(inverse_distance)
        ax0.plot(
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
ax0.set_xlabel('Inverse Center of Mass Distance (1/Å)')
ax0.set_ylabel('$V_C$ (eV)')
ax0.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax0.legend(fontsize=6, loc='upper right', frameon=False)

# Set x-axis limits based on the data range
inverse_distance_min = min(all_inverse_distances)
inverse_distance_max = max(all_inverse_distances)
ax0.set_xlim(inverse_distance_min, inverse_distance_max)

# Create a secondary x-axis on top that shares the same scale (for direct distances)
secax = ax0.twiny()
secax.set_xlim(ax0.get_xlim())
secax.set_xlabel('Center of Mass Distance (Å)', fontsize=7)
secax.tick_params(axis='both', which='major', labelsize=7)

# Set ticks on the secondary x-axis at positions corresponding to distances 4, 5, 6, 10, and 20 Å
distance_ticks = [3, 4, 5, 6, 10, 20]  # Distances in Ångströms
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
ax0.legend(
    fontsize=6,
    loc='upper right',
    frameon=False,
    handletextpad=0.3,
    borderpad=0.3,
    labelspacing=0.3
)

# --- Plot b (Combined plot with embedded points and two y-axes) ---
# Use ax1

# Read the first_rdf_peak data
rdf_peak_df = pd.read_csv('../../simulations/summary/Deposit/first_rdf_peak.csv')
rdf_peak_df['material_clean'] = rdf_peak_df['material'].apply(lambda x: x.split('_')[0])
rdf_peak_df.set_index('material', inplace=True)

# Initialize a list to store results
results = []

# Process each material
for material in rdf_peak_df.index:
    first_rdf_peak = rdf_peak_df.loc[material, 'first_rdf_peak']
    clean_name = rdf_peak_df.loc[material, 'material_clean']

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

# Sort the DataFrame by 'first_rdf_peak' for consistent plotting
results_df.sort_values(by='first_rdf_peak', inplace=True)

# Set up x positions
materials = results_df['material']
first_rdf_peak = results_df['first_rdf_peak']
VC_mean = results_df['VC_mean']

x = np.arange(len(materials))
bar_width = 0.4

# Plot 'first_rdf_peak' as bars on ax1
bars = ax1.bar(x, first_rdf_peak, width=bar_width, color='dodgerblue', edgecolor='black')
ax1.set_ylabel('First RDF Peak (Å)', color='dodgerblue')
ax1.tick_params(axis='y', labelcolor='dodgerblue')

# Set y-axis limits to start at 3 Å for the RDF Peak
ax1.set_ylim(4, first_rdf_peak.max() + 1)  # Adjust the upper limit as needed

# Create a secondary axis for VC_mean
ax1_twin = ax1.twinx()

# Plot 'VC_mean' as scatter points inside the bars
ax1_twin.scatter(x, VC_mean, color='darkred', marker='o', zorder=5)
ax1_twin.set_ylabel('$V_C$ at First RDF Peak (eV)', color='darkred')
ax1_twin.tick_params(axis='y', labelcolor='darkred')

# Set x-axis labels
ax1.set_xticks(x)
ax1.set_xticklabels(materials, rotation=45, ha='right')

# Adjust layout for better spacing and alignment
plt.tight_layout()

# --- Plot c (old Figure d) ---
# Use ax2

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
# exp_data.rename(columns={'material_name': 'base_material', 'efficiency': 'efficiency_exp'}, inplace=True)

# Merge simulated data with VC data on `base_material`
sim_data = pd.merge(sim_data, vc_data[['base_material', 'VC_mean']], on='base_material', how='inner')


ax2.set_xlabel('IP - EA + $V_C$ (eV)')
ax2.set_ylabel(r'Ionization Fraction  $\eta_{\mathrm{exper}}$')


# --- Add the derivative line from panel b of the second script ---
# Specify the material for which you want to add the derivative line
material_name = 'm-MTDATA@F4TCNQ_0.02'  # Corresponds to material number 4

# Path to the CSV file for the material in the second script
csv_path = '../../simulations/summary/Lightforge/fictional_materials/{}.csv'.format(material_name)


if os.path.exists(csv_path):
    # Read the CSV file
    df_ionization_fictional_material = pd.read_csv(csv_path)

    # Sort the DataFrame by ionization fraction in increasing order
    df_ionization_fictional_material.sort_values(by='IP', inplace=True)

    # Compute IP - EA Difference
    df_ionization_fictional_material['IP_EA_diff'] = df_ionization_fictional_material['IP'] - df_ionization_fictional_material['EA']

    # Get VC_mean for the base material
    base_material = material_name.split('_')[0]
    vc_mean_row = vc_data[vc_data['base_material'] == base_material]
    if not vc_mean_row.empty:
        vc_mean = vc_mean_row['VC_mean'].values[0]
    else:
        print(f"VC_mean not found for {base_material}")
        vc_mean = 0  # Default to 0 if not found

    # Adjust IP_EA_diff by adding VC_mean to get IP - EA + VC
    df_ionization_fictional_material['IP_EA_VC'] = df_ionization_fictional_material['IP_EA_diff'] + vc_mean

    # Extract x (IP - EA + VC) and y (ionization fraction)
    IP_minus_EA = df_ionization_fictional_material['IP_EA_VC'].values

    #


    ionization_fraction = df_ionization_fictional_material['ionization'].values

    ax2.plot(IP_minus_EA, ionization_fraction, color='black', linestyle='-', label=material_name.split("_")[0])  # ionization fraction

    # Compute the derivative d(IP - EA + VC)/dη using central difference
    def central_difference(x, y):
        dydx = np.zeros_like(y)
        dydx[1:-1] = (x[2:] - x[:-2]) / (y[2:] - y[:-2])
        dydx[0] = (x[1] - x[0]) / (y[1] - y[0])
        dydx[-1] = (x[-1] - x[-2]) / (y[-1] - y[-2])
        return dydx

    derivative = central_difference(IP_minus_EA, ionization_fraction)  # dx/dy

    # Convert derivative to kcal/mol per %
    derivative_kcal_per_percent = derivative * 23.0609 / 100   # eV/fraction to kcal/mol / %



    # Create secondary y-axis
    ax_secondary = ax2.twinx()
    ax_secondary.set_ylabel('d(IP - EA + $V_C$)/d$\eta$ (kcal/mol/%)', color='grey', fontsize=7)
    ax_secondary.tick_params(axis='y', labelcolor='grey')

    # Plot the derivative line
    ax_secondary.plot(IP_minus_EA, derivative_kcal_per_percent, color='grey', linestyle='-', label='Derivative')

    ax_secondary.set_ylim([-1.5, 0])

    # Adjust x-limits to match ax2
    ax_secondary.set_xlim(ax2.get_xlim())

    # Add the derivative line to the legend
    ax2.legend(loc='upper left', frameon=False)

    ax2.set_ylim([0.0, 1.0])
    ax2.set_xlim([-0.75, 0.5])

    ax2.plot([0.0, 0.0], [0.0, 1.0], linestyle='--', color='grey')

else:
    print(f"CSV file for {material_name} not found at {csv_path}")

# Adjust layout to make sure everything fits nicely
plt.tight_layout(pad=1.0)

# Save the figure in high-resolution PNG and PDF formats
plt.savefig('figure_4_abc.png', dpi=600, bbox_inches='tight')
plt.savefig('figure_4_abc.pdf', dpi=600, bbox_inches='tight')

# Display the plot
plt.show()
