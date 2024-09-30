import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import yaml
import os

# General Formatting for All Plots
mpl.rcParams['font.family'] = ['Arial', 'Helvetica', 'sans-serif']
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
mpl.rcParams['legend.fontsize'] = 7
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['lines.markersize'] = 4

# Figure Size (width x height in inches)
full_page_width = 7.08  # Full page width in inches (18 cm)
fig_width = full_page_width  # Total figure width
fig_height = full_page_width * (3/4)  # Adjust height to maintain aspect ratio

# Create a 2×2 Grid of Subplots
fig, axes = plt.subplots(2, 2, figsize=(fig_width, fig_height))

# Flatten axes array for easy indexing
axes = axes.flatten()

### Plot A ###
# Use axes[0] for subplot (a)
# Read data
df_a = pd.read_csv('../../simulations/summary/Deposit/first_rdf_peak.csv')
df_a['material_clean'] = df_a['material'].apply(lambda x: x.split('_')[0])
df_a_sorted = df_a.sort_values(by='first_rdf_peak')

# Plotting on axes[0]
axes[0].bar(df_a_sorted['material_clean'], df_a_sorted['first_rdf_peak'],
            color='skyblue', edgecolor='black')

# Customize subplot (a)
axes[0].set_xlabel('Material')
axes[0].set_ylabel('First RDF Peak (Å)')
axes[0].set_xticklabels(df_a_sorted['material_clean'], rotation=45, ha='right')
axes[0].set_ylim(4, None)
axes[0].set_title('(a) First RDF Peak vs. Material', fontsize=8)

### Plot B ###
# Use axes[1] for subplot (b)
# Load data from YAML
yaml_file_path = '../../simulations/summary/QuantumPatch/merged_vc_data.yaml'

if not os.path.isfile(yaml_file_path):
    # Handle the case where the YAML file doesn't exist
    raise FileNotFoundError(f"{yaml_file_path} not found.")

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
            markersize=4,
            color=colors[idx % len(colors)],
            label=folder_labels.get(material, material),
            alpha=0.5
        )
    else:
        print(f"Data for {material} not found in the YAML file.")

# Customize subplot (b)
axes[1].set_xlabel('Inverse Center of Mass Distance (1/Å)')
axes[1].set_ylabel('$V_C$ (eV)')
axes[1].set_title('(b) $V_C$ vs. Inverse Distance', fontsize=8)
axes[1].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
axes[1].legend(fontsize=6, loc='upper right', frameon=False)

# Adjust x-axis limits
inverse_distance_min = min(all_inverse_distances)
inverse_distance_max = max(all_inverse_distances)
axes[1].set_xlim(inverse_distance_min, inverse_distance_max)

### Plot C ###
# Use axes[2] for subplot (c)
# Read the RDF peak data
rdf_peak_file = '../../simulations/summary/Deposit/first_rdf_peak.csv'
rdf_peak_df = pd.read_csv(rdf_peak_file)
rdf_peak_df['clean_material'] = rdf_peak_df['material'].apply(lambda x: x.split('_')[0])

# Read the VC data from YAML
vc_data = []
for material in rdf_peak_df['material']:
    clean_material = material.split('_')[0]
    first_rdf_peak = rdf_peak_df.loc[rdf_peak_df['material'] == material, 'first_rdf_peak'].values[0]
    if material in merged_data:
        data = pd.DataFrame({
            'dimer_comdist': merged_data[material]['inverse_distance'],
            'VC_corrected': merged_data[material]['VC_corrected']
        })
        data['dimer_comdist'] = 1 / data['dimer_comdist']  # Convert to distance
        # Find the VC at the first RDF peak
        vc_at_peak = data.iloc[(data['dimer_comdist'] - first_rdf_peak).abs().argsort()[:1]]['VC_corrected'].values[0]
        vc_data.append({'material': clean_material, 'VC_mean': vc_at_peak})
    else:
        print(f"Data for {material} not found.")

vc_df = pd.DataFrame(vc_data)
vc_df.sort_values(by='VC_mean', inplace=True)

# Plotting on axes[2]
axes[2].barh(vc_df['material'], vc_df['VC_mean'], color='skyblue')
axes[2].set_xlabel('$V_C$ at First RDF Peak (eV)')
axes[2].set_ylabel('Material')
axes[2].set_title('(c) $V_C$ at First RDF Peak', fontsize=8)
axes[2].set_xlim([-0.9, -0.6])

### Plot D ###
# Use axes[3] for subplot (d)
# Read simulated and experimental data
sim_data = pd.read_csv('../../simulations/summary/Lightforge/ionization_ip_ea.csv')
exp_data = pd.read_csv('../../experimental_data/summary/measured_efficiency.csv')
vc_data = vc_df[['material', 'VC_mean']]

# Merge data
merged_data_d = pd.merge(sim_data, vc_data, left_on='material', right_on='material')
merged_data_d = pd.merge(merged_data_d, exp_data, left_on='material', right_on='material_name')

# Calculate IP - EA + VC
merged_data_d['IP_EA_VC_sim'] = merged_data_d['IP'] - merged_data_d['EA'] + merged_data_d['VC_mean']

# Plotting on axes[3]
axes[3].scatter(merged_data_d['IP_EA_VC_sim'], merged_data_d['efficiency'], color='blue', marker='o', label='Simulated')
axes[3].scatter(merged_data_d['IP_EA_VC_sim'], merged_data_d['efficiency_exp'], color='red', marker='s', label='Experimental')

# Customize subplot (d)
axes[3].set_xlabel('IP - EA + $V_C$ (Simulated) [eV]')
axes[3].set_ylabel(r'Ionization Fraction $\eta_{\mathrm{exper}}$')
axes[3].set_title('(d) Doping Efficiency vs. IP - EA + $V_C$', fontsize=8)
axes[3].legend(fontsize=7)
axes[3].set_ylim(bottom=0.0)

# Adjust Layout
plt.tight_layout(pad=1.0)

# Save the Combined Figure
plt.savefig('combined_figure.png', dpi=600, bbox_inches='tight')
plt.savefig('combined_figure.pdf', dpi=600, bbox_inches='tight')

# Show the Plot (optional)
plt.show()
