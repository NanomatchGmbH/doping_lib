import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl
from matplotlib import cm

# Set up paths
input_dir = '../../../../simulations/summary/Lightforge/fictional_materials'  # Directory where CSV files are located
actual_data_file = '../../../../simulations/summary/Lightforge/ionization_ip_ea.csv'  # File with actual data points
output_dir = '../../../../simulations/summary/Lightforge/fictional_materials'  # Directory to save the plots
os.makedirs(output_dir, exist_ok=True)

# Conversion toggle for y-axis in the second plot
use_kcal_per_mol_y_axis = True  # Set to True to convert the derivative units to %/kcal/mol

# Conversion factor from eV to kcal/mol
eV_to_kcal_per_mol = 23.0609

# Load all CSV files from the input directory
csv_files = [f.replace('.csv', '') for f in os.listdir(input_dir) if f.endswith('.csv')]  # Remove .csv extension from filenames

# Create a list to hold dataframes and corresponding material names
dataframes = []
material_names = []

# Read each CSV file and store the dataframe and corresponding material name
for file in csv_files:
    df = pd.read_csv(os.path.join(input_dir, file + '.csv'))
    dataframes.append(df)
    material_names.append(file)

# Calculate IP - EA difference for each dataset
for df in dataframes:
    df['IP_EA_diff'] = df['IP'] - df['EA']
    df.sort_values(by='IP_EA_diff', inplace=True)  # Sort data based on IP - EA difference

# Read the actual data
actual_data = pd.read_csv(actual_data_file)

# Create a mapping from numbers to materials, adding those without csv files
materials_info = [
    {'Number': 1, 'Material': 'BFDPB@CN6-CP_0.26'},
    {'Number': 2, 'Material': 'NPB@CN6-CP_0.26'},
    {'Number': 3, 'Material': 'BPAPF@CN6-CP_0.26'},
    {'Number': 4, 'Material': 'TCTA@CN6-CP_0.26'},
    {'Number': 5, 'Material': 'CBP@CN6-CP_0.07'},
    {'Number': 6, 'Material': 'MeO-TPD@F4TCNQ_0.02'},
    {'Number': 7, 'Material': 'm-MTDATA@F4TCNQ_0.02'},
    {'Number': 8, 'Material': 'TPD@F4TCNQ_0.02'},
    {'Number': 9, 'Material': 'TCTA@F6TCNNQ'}
]

# Create a mapping from material to number
material_numbers = {item['Material']: item['Number'] for item in materials_info}

# Get the materials without CSV files
materials_without_csv = [item['Material'] for item in materials_info if item['Material'] not in material_names]

# Plot settings for Advanced Materials journal style
mpl.rcParams['font.family'] = ['Arial', 'Helvetica', 'sans-serif']
full_page_width = 7.08  # Full-page width for the journal (7.08 inches)
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
mpl.rcParams['legend.fontsize'] = 7

# Create the figure with two subplots (a) and (b)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(full_page_width, 4.5))  # Full-page width and height adjustment

# Use a vibrant color palette (Set1) or another scientific palette (like cmocean)
colors = cm.get_cmap('Set1', len(dataframes))  # Get a color palette with distinct colors for each dataset

# ---------------------------------------------------
# Left plot (a): Ionization vs IP - EA Difference
# ---------------------------------------------------
for i, df in enumerate(dataframes):
    material_label = material_names[i]
    # Plot the lines for the material (sorted data)
    ax1.plot(df['IP_EA_diff'], df['ionization'], color=colors(i), label=material_label, linestyle='-', marker='')

# Plot actual data points for matching materials and annotate with numbers
for idx, row in actual_data.iterrows():
    material = row['material']
    # Check if the material is in our materials_info
    material_number = material_numbers.get(material, None)
    if material_number is not None:
        ip_ea_diff = row['IP'] - row['EA']
        efficiency = row['efficiency']
        # Find the color corresponding to this material in the datasets
        if material in material_names:
            i = material_names.index(material)
            color = colors(i)
        else:
            continue  # Skip if no matching material is found in the CSV files
        # Plot the actual data point
        ax1.scatter(ip_ea_diff, efficiency, color=color, marker='o', s=50)
        # Annotate the point with the number
        ax1.annotate(str(material_number), (ip_ea_diff, efficiency), textcoords="offset points",
                     xytext=(5, 5), ha='left', fontsize=8, fontstyle='italic')

# Plot hollow points for materials without CSV files
for item in materials_info:
    material = item['Material']
    material_number = item['Number']
    if material in materials_without_csv:
        matching_row = actual_data[actual_data['material'] == material]
        if not matching_row.empty:
            ip_ea_diff = matching_row['IP'].values[0] - matching_row['EA'].values[0]
            efficiency = matching_row['efficiency'].values[0]
            # Find the color of a material with the same ionization fraction
            similar_material = None
            fraction = material.split('_')[-1]
            for other_material in material_names:
                if other_material.endswith(fraction):
                    similar_material = other_material
                    break
            if similar_material:
                i = material_names.index(similar_material)
                color = colors(i)
            else:
                continue  # Skip if no similar material is found
            # Plot the hollow point
            ax1.scatter(ip_ea_diff, efficiency, facecolors='none', edgecolors=color, marker='o', s=50)
            # Annotate the hollow point with the number
            ax1.annotate(str(material_number), (ip_ea_diff, efficiency), textcoords="offset points",
                         xytext=(5, 5), ha='left', fontsize=8, fontstyle='italic')

# Add labels and title for plot (a)
ax1.set_xlabel('IP - EA Difference [eV]')
ax1.set_ylabel(r'Ionization Fraction  $\eta_{\mathrm{sim}}$')

ax1.set_ylim([0.0, 1.0])

# Add a legend for plot (a)
handles, labels = ax1.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))  # Remove duplicate labels
ax1.legend(unique_labels.values(), unique_labels.keys(), loc='best')

# ---------------------------------------------------
# Right plot (b): Derivative of IP - EA vs Ionization
# ---------------------------------------------------
for i, df in enumerate(dataframes):
    # Calculate the derivative d(IP - EA)/d(η)
    df['d_ip_ea'] = np.gradient(df['IP_EA_diff'], df['ionization']*100)  # Derivative of IP - EA wrt ionization

    # If kcal/mol is used for y-axis, apply the conversion factor
    if use_kcal_per_mol_y_axis:
        df['d_ip_ea'] *= eV_to_kcal_per_mol  # Convert to kcal/mol

    # Plot the reversed derivative
    ax2.plot(df['IP_EA_diff'], df['d_ip_ea'], color=colors(i), label=material_names[i], linestyle='-', marker='')

# Add labels and title for plot (b)
y_label_unit = 'kcal/mol' if use_kcal_per_mol_y_axis else 'eV'
ax2.set_xlabel('IP - EA Difference [eV]')  # x-axis remains in eV
ax2.set_ylabel(f'd(IP - EA)/d($\eta_{{\mathrm{{sim}}}}$) [{y_label_unit}/%]')

# Add a legend for plot (b)
handles, labels = ax2.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))  # Remove duplicate labels
ax2.legend(unique_labels.values(), unique_labels.keys(), loc='best')

ax2.set_ylim([-1, 1])  # Adjust the y-limits as needed
# ax2.set_xlim([-0.5, 1])  # Adjust the y-limits as needed

# Adjust layout to add the labels (a) and (b)
ax1.text(-0.15, 1.05, "a", transform=ax1.transAxes, fontsize=12, fontweight='bold')
ax2.text(-0.15, 1.05, "b", transform=ax2.transAxes, fontsize=12, fontweight='bold')

# Adjust the layout to make sure everything fits nicely
plt.tight_layout()

# Save the full figure as both PNG and PDF
plot_png = os.path.join(output_dir, 'ionization_derivative_plots_inv.png')
plot_pdf = os.path.join(output_dir, 'ionization_derivative_plots_inv.pdf')

plt.savefig(plot_png, dpi=300)  # Save as PNG
plt.savefig(plot_pdf)           # Save as PDF

# Show the full figure
plt.show()
