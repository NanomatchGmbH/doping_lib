import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the simulated data
sim_data = pd.read_csv('../../simulations/summary/Lightforge/ionization_ip_ea.csv')

# Read the experimental data
exp_data = pd.read_csv('../../experimental_data/summary/measured_efficiency.csv')

# Extract base material names from simulated data
def extract_base_material(material):
    # Remove the fraction part (e.g., '@CN6-CP_0.26' -> '@CN6-CP')
    if '@' in material:
        base_material = material.split('_')[0]
    else:
        base_material = material
    return base_material

sim_data['base_material'] = sim_data['material'].apply(extract_base_material)

# Prepare the experimental data
exp_data.rename(columns={'material_name': 'base_material', 'efficiency': 'efficiency_exp'}, inplace=True)

# Merge datasets on 'base_material'
merged_data = pd.merge(sim_data, exp_data[['base_material', 'efficiency_exp']], on='base_material', how='inner')

# Compute IP - EA (from simulations)
merged_data['IP_EA_sim'] = merged_data['IP'] - merged_data['EA']

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
    1: 0.969025613,
    2: 0.921286021,
    3: 0.848504597,
    4: 0.800000000  # Example for material 4, you can modify this value
}

# Create a directory to save the plots if it doesn't exist
output_dir = '../../exper_vs_sim/'
os.makedirs(output_dir, exist_ok=True)

# Plot settings for Advanced Materials journal
import matplotlib as mpl

# Set font family to Arial (or Helvetica)
mpl.rcParams['font.family'] = ['Arial', 'Helvetica', 'sans-serif']

# Set figure size (width x height) in inches (1 inch = 2.54 cm)
# For half-page width (approximately 8.5 cm), set width to 3.35 inches
figure_width = 3.35  # inches
figure_height = 2.5  # Adjust height as needed

# Set font sizes according to the journal's guidelines
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
mpl.rcParams['legend.fontsize'] = 7

# --------------------------------------------
# Plot 1: Doping Efficiency vs IP - EA (Simulated)
# --------------------------------------------

plt.figure(figsize=(figure_width, figure_height))

# Plot simulated doping efficiency
plt.scatter(merged_data['IP_EA_sim'], merged_data['efficiency'], color='blue', marker='o', label='Simulated')

# Plot experimental doping efficiency
plt.scatter(merged_data['IP_EA_sim'], merged_data['efficiency_exp'], color='red', marker='s', label='Experimental')

# Add unfilled circles for relative simulation values for materials 1-4
for i in range(1, 5):
    material_row = merged_data[merged_data['material_number'] == i]
    if not material_row.empty:
        plt.scatter(material_row['IP_EA_sim'], relative_simulation_values[i], facecolors='none', edgecolors='blue', marker='o')

plt.xlabel('IP - EA (Simulated) [eV]')
plt.ylabel(r'Ionization Fraction  $\eta_{\mathrm{exper}}$')
plt.legend()

# Annotate data points with italic numbers
for i, row in merged_data.iterrows():
    plt.annotate(str(row['material_number']), (row['IP_EA_sim'], row['efficiency']), textcoords="offset points",
                 xytext=(5, -5), fontsize=7, color='blue', fontstyle='italic')
    plt.annotate(str(row['material_number']), (row['IP_EA_sim'], row['efficiency_exp']), textcoords="offset points",
                 xytext=(5, 5), fontsize=7, color='red', fontstyle='italic')

plt.axis('square')


# Restrict y-axis to start from 0.0
plt.ylim(bottom=0.0)

# Adjust layout
plt.tight_layout()

# Save the plot
plot_filename = os.path.join(output_dir, 'doping_efficiency_vs_IP_EA.png')
plt.savefig(plot_filename, dpi=300)

plt.show()

# --------------------------------------------
# Plot 2: Simulated vs Experimental Doping Efficiency
# --------------------------------------------

# Square plot settings
figure_height = figure_width  # Ensure square dimensions

plt.figure(figsize=(figure_width, figure_height))

# Scatter plot
plt.scatter(merged_data['efficiency_exp'], merged_data['efficiency'], color='green', marker='o')

# Plot x=y line
max_efficiency = max(merged_data['efficiency'].max(), merged_data['efficiency_exp'].max())
plt.plot([0, max_efficiency], [0, max_efficiency], 'k--')

plt.xlabel(r'Experimental Ionization Fraction, $\eta_{\mathrm{exper}}$')
plt.ylabel(r'Simulated Ionization Fraction, $\eta_{\mathrm{sim}}$')
# plt.legend()

# Annotate data points with italic numbers
for i, row in merged_data.iterrows():
    plt.annotate(str(row['material_number']), (row['efficiency_exp'], row['efficiency']), textcoords="offset points",
                 xytext=(5, -5), fontsize=7, fontstyle='italic')

# Set equal aspect ratio
plt.axis('square')
plt.xlim(0, max_efficiency * 1.1)
plt.ylim(0, max_efficiency * 1.1)

# Restrict y and x axes to start from 0.0
plt.xlim(left=0.0)
plt.ylim(bottom=0.0)

# Adjust layout
plt.tight_layout()

# Save the plot
plot_filename = os.path.join(output_dir, 'simulated_vs_experimental_doping_efficiency.png')
plt.savefig(plot_filename, dpi=300)

plt.show()

# --------------------------------------------
# Generate the table mapping numbers to materials
# --------------------------------------------

# Create the table data
table_data = []

for item in materials_info:
    num = item['Number']
    material = item['Material']
    mol_percent = item['mol%']
    # Try to find matching data in merged_data
    data_rows = merged_data[merged_data['material_number'] == num]
    if not data_rows.empty:
        efficiency_exp = data_rows['efficiency_exp'].values[0]
        efficiency_sim = data_rows['efficiency'].values[0]
    else:
        # Data not available in merged_data
        efficiency_exp_row = exp_data[exp_data['base_material'] == material]
        efficiency_exp = efficiency_exp_row['efficiency_exp'].values[0] if not efficiency_exp_row.empty else 'n.d.'
        efficiency_sim = 'n.d.'
    table_data.append({
        'Number': num,
        'Material (<host>@<dopant>)': material,
        'mol%': mol_percent,
        'η_exp': efficiency_exp,
        'η_sim': efficiency_sim
    })

# Create DataFrame
table_df = pd.DataFrame(table_data, columns=['Number', 'Material (<host>@<dopant>)', 'mol%', 'η_exp', 'η_sim'])

# Print the table
print(table_df.to_string(index=False))

# Save the table
table_df.to_csv(os.path.join(output_dir, 'material_numbers_table.csv'), index=False)
