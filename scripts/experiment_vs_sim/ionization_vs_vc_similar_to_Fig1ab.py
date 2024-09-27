import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the simulated data (IP, EA) and VC data from CSV file
sim_data = pd.read_csv('../../simulations/summary/Lightforge/ionization_ip_ea.csv')

# Read the VC data, which includes `VC_mean`
vc_data = pd.read_csv('../../simulations/summary/Deposit/VC_at_first_rdf_peak.csv')  # Update this path to your actual CSV file

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

# Relative simulation values for materials 1 to 4
relative_simulation_values = {
    1: 1.0,
    2: 0.969025613,
    3: 0.921286021,
    4: 0.848504597
}

# Create a directory to save the plots if it doesn't exist
output_dir = '../../exper_vs_sim/'
os.makedirs(output_dir, exist_ok=True)

# Plot settings for Advanced Materials journal
import matplotlib as mpl

mpl.rcParams['font.family'] = ['Arial', 'Helvetica', 'sans-serif']
half_page_width = 7.08 / 2  # Set to half of full page width (7.08 inches for full width)
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
mpl.rcParams['legend.fontsize'] = 7

# Create a figure for the left plot only (half width)
fig, ax1 = plt.subplots(figsize=(half_page_width, 4.5))  # Adjust height as needed

# --------------------------------------------
# Plot: Doping Efficiency vs IP - EA + VC (Simulated)
# --------------------------------------------

# Plot simulated doping efficiency
ax1.scatter(merged_data['IP_EA_VC_sim'], merged_data['efficiency'], color='blue', marker='o', label='Simulated')

# Plot experimental doping efficiency
ax1.scatter(merged_data['IP_EA_VC_sim'], merged_data['efficiency_exp'], color='red', marker='s', label='Experimental')

# Add unfilled circles for relative simulation values for materials 1-4
for i in range(1, 5):
    material_row = merged_data[merged_data['material_number'] == i]
    if not material_row.empty:
        ax1.scatter(material_row['IP_EA_VC_sim'], relative_simulation_values[i], facecolors='none', edgecolors='blue', marker='o', label='Sim. (relative)' if i == 1 else "")

ax1.set_xlabel('IP - EA + VC (Simulated) [eV]')
ax1.set_ylabel(r'Ionization Fraction  $\eta_{\mathrm{exper}}$')
ax1.legend()

# Annotate data points with italic numbers
for i, row in merged_data.iterrows():
    ax1.annotate(str(row['material_number']), (row['IP_EA_VC_sim'], row['efficiency']), textcoords="offset points",
                 xytext=(5, -5), fontsize=7, color='blue', fontstyle='italic')
    ax1.annotate(str(row['material_number']), (row['IP_EA_VC_sim'], row['efficiency_exp']), textcoords="offset points",
                 xytext=(5, 5), fontsize=7, color='red', fontstyle='italic')

# Restrict y-axis to start from 0.0
ax1.set_ylim(bottom=0.0)

# Adjust layout to make sure everything fits nicely
plt.tight_layout()

# Save the plot
plot_filename = os.path.join(output_dir, 'doping_efficiency_vs_ipeavc_single_plot.png')
plt.savefig(plot_filename, dpi=300)

plt.show()
