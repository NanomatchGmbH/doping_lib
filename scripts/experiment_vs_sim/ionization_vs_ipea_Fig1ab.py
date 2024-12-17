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
    1: 1.0,
    2: 0.969025613,
    3: 0.921286021,
    4: 0.848504597  # Example for material 4, you can modify this value
}

# Create a directory to save the plots if it doesn't exist
output_dir = '../../exper_vs_sim/'
os.makedirs(output_dir, exist_ok=True)

# Plot settings for Advanced Materials journal
import matplotlib as mpl

# Set font family to Arial (or Helvetica)
mpl.rcParams['font.family'] = ['Arial', 'Helvetica', 'sans-serif']

# Set figure size (width x height) in inches (1 inch = 2.54 cm)
# For full-page width in the journal, each plot takes half of a full page width (approximately 18 cm wide)
full_page_width = 7.08  # inches (full page width)
half_page_width = full_page_width / 2  # Each plot gets half the page width

# Set font sizes according to the journal's guidelines
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
mpl.rcParams['legend.fontsize'] = 7

# --------------------------------------------
# Create a figure with two subplots side by side (a) and (b)
# --------------------------------------------

fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(full_page_width, 4.5))  # Adjust height as needed

# --------------------------------------------
# Plot 2: Doping Efficiency vs IP - EA (Simulated) in ax2
# --------------------------------------------

# Plot experimental doping efficiency
ax1.scatter(merged_data['IP_EA_sim'], merged_data['efficiency_exp'], color=plt.cm.tab10(3), marker='s',  label=r'Experimental $\eta_{\mathrm{exp}}$')

# Plot simulated doping efficiency
ax1.scatter(merged_data['IP_EA_sim'], merged_data['efficiency'], color=plt.cm.tab10(0), marker='o',  label=r'Simulated $\eta_{\mathrm{sim}}$')

# Add unfilled circles for relative simulation values for materials 1-4
for i in range(1, 5):
    material_row = merged_data[merged_data['material_number'] == i]
    if not material_row.empty:
        ax1.scatter(material_row['IP_EA_sim'], relative_simulation_values[i], facecolors='none', edgecolors=plt.cm.tab10(0),
                    marker='o', label=r'Simulated $\eta_{\mathrm{sim,rel}}$' if i == 1 else "")

# Add unfilled circles for relative simulation values for materials 1-4
for i in range(1, 5):
    material_row = merged_data[merged_data['material_number'] == i]
    if not material_row.empty:
        ax1.annotate(str(i), (material_row['IP_EA_sim'].values[0], relative_simulation_values[i]), textcoords="offset points",
                     xytext=(5, 5), fontsize=7, color=plt.cm.tab10(0), fontstyle='italic')

ax1.set_xlabel('IP - EA (Simulated) [eV]')
ax1.set_ylabel(r'Ionization Fraction, $\eta$')
ax1.legend()

# Annotate data points with italic numbers
for i, row in merged_data.iterrows():
    ax1.annotate(str(row['material_number']), (row['IP_EA_sim'], row['efficiency']), textcoords="offset points",
                 xytext=(5, -5), fontsize=7, color=plt.cm.tab10(0), fontstyle='italic')
    ax1.annotate(str(row['material_number']), (row['IP_EA_sim'], row['efficiency_exp']), textcoords="offset points",
                 xytext=(5, 5), fontsize=7, color=plt.cm.tab10(3), fontstyle='italic')

# Restrict y-axis to start from 0.0
ax1.set_ylim(bottom=0.0)

# Add label "a" for figure part A
ax1.text(-0.15, 1.05, "b", transform=ax1.transAxes, fontsize=12, fontweight='bold')

# --------------------------------------------
# Plot 1: Simulated vs Experimental Doping Efficiency in ax1
# --------------------------------------------

# Scatter plot
ax2.scatter(merged_data['efficiency_exp'], merged_data['efficiency'], color=plt.cm.tab10(2), marker='o')

# Plot x=y line
max_efficiency = max(merged_data['efficiency'].max(), merged_data['efficiency_exp'].max())
ax2.plot([0, max_efficiency], [0, max_efficiency], 'k--')

ax2.set_xlabel(r'Experimental Ionization Fraction, $\eta_{\mathrm{exp}}$')
ax2.set_ylabel(r'Simulated Ionization Fraction, $\eta_{\mathrm{sim}}$')

# Add unfilled circles for relative simulation values for materials 1-4
for i in range(1, 5):
    material_row = merged_data[merged_data['material_number'] == i]
    if not material_row.empty:
        ax2.scatter(material_row['efficiency_exp'], relative_simulation_values[i], facecolors='none', edgecolors=plt.cm.tab10(2), marker='o', label='Sim. (relative)' if i == 1 else "")

# Annotate data points with italic numbers
for i, row in merged_data.iterrows():
    ax2.annotate(str(row['material_number']), (row['efficiency_exp'], row['efficiency']), textcoords="offset points",
                 xytext=(5, -5), fontsize=7, fontstyle='italic')

# Annotate hollow points with italic numbers for Panel A (ax2)
for i in range(1, 5):
    material_row = merged_data[merged_data['material_number'] == i]
    if not material_row.empty:
        efficiency_exp = material_row['efficiency_exp'].values[0]  # Experimental efficiency
        relative_efficiency = relative_simulation_values[i]  # Relative simulated efficiency
        ax2.annotate(str(i), (efficiency_exp, relative_efficiency),
                     textcoords="offset points", xytext=(-5, 5),  # Adjust for left-upper position
                     fontsize=7, color='black', fontstyle='italic')

# Set equal aspect ratio
ax2.set_aspect('equal', 'box')
ax2.set_xlim(0, max_efficiency * 1.1)
ax2.set_ylim(0, max_efficiency * 1.1)

# Restrict y and x axes to start from 0.0
ax2.set_xlim(left=0.0)
ax2.set_ylim(bottom=0.0)

# Add label "b" for figure part B
ax2.text(-0.15, 1.05, "a", transform=ax2.transAxes, fontsize=12, fontweight='bold')

# Adjust layout to make sure everything fits nicely
plt.tight_layout()

# Save the combined plot
plot_filename = os.path.join(output_dir, 'Fig2.png')
plt.savefig(plot_filename, dpi=600)
plot_filename = os.path.join(output_dir, 'Fig2.pdf')
plt.savefig(plot_filename)

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
