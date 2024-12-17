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
vc_dir = '../../../../simulations/summary/Deposit/VC_at_first_rdf_peak.csv'

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

# Read the VC data
vc_df = pd.read_csv(vc_dir)

# Create a dictionary to map materials to their VC values
vc_dict = dict(zip(vc_df['material'], vc_df['VC_mean']))

# Load the actual data and merge with VC data
actual_data = pd.read_csv(actual_data_file)
actual_data = pd.merge(actual_data, vc_df[['material', 'VC_mean']], on='material', how='left')

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

# Calculate IP - EA + VC difference for each dataset
for i, (df, material_name) in enumerate(zip(dataframes, material_names)):
    # Add 'VC' to df
    if material_name in vc_dict:
        df['VC'] = vc_dict[material_name]
    else:
        print(f"Warning: {material_name} not found in VC data.")
        df['VC'] = np.nan
    # Calculate IP - EA + VC difference
    df['IP_EA_VC_diff'] = df['IP'] - df['EA'] + df['VC']
    df.sort_values(by='IP_EA_VC_diff', inplace=True)  # Sort data based on IP - EA + VC difference

# ---------------------------------------------------
# Left plot (a): Ionization vs IP - EA + VC Difference
# ---------------------------------------------------
for i, df in enumerate(dataframes):
    material_label = material_names[i]
    # Plot the lines for the material (sorted data)
    ax1.plot(df['IP_EA_VC_diff'], df['ionization'], color=colors(i), label=material_label, linestyle='-', marker='')

# Plot actual data points for matching materials and annotate with numbers
for idx, row in actual_data.iterrows():
    material = row['material']
    # Check if the material is in our materials_info
    material_number = material_numbers.get(material, None)
    if material_number is not None:
        # Calculate IP - EA + VC difference
        if pd.notna(row['VC_mean']):
            ip_ea_vc_diff = row['IP'] - row['EA'] + row['VC_mean']
        else:
            print(f"Warning: VC_mean missing for material {material}")
            ip_ea_vc_diff = row['IP'] - row['EA']
        efficiency = row['efficiency']
        # Find the color corresponding to this material in the datasets
        if material in material_names:
            i = material_names.index(material)
            color = colors(i)
        else:
            continue  # Skip if no matching material is found in the CSV files
        # Plot the actual data point
        ax1.scatter(ip_ea_vc_diff, efficiency, color=color, marker='o', s=50)
        # Annotate the point with the number
        ax1.annotate(str(material_number), (ip_ea_vc_diff, efficiency), textcoords="offset points",
                     xytext=(5, 5), ha='left', fontsize=8, fontstyle='italic')

# Plot hollow points for materials without CSV files
for item in materials_info:
    material = item['Material']
    material_number = item['Number']
    if material in materials_without_csv:
        matching_row = actual_data[actual_data['material'] == material]
        if not matching_row.empty:
            # Calculate IP - EA + VC difference
            ip_ea_diff = matching_row['IP'].values[0] - matching_row['EA'].values[0]
            vc_mean = matching_row['VC_mean'].values[0]
            if not np.isnan(vc_mean):
                ip_ea_vc_diff = ip_ea_diff + vc_mean
            else:
                print(f"Warning: VC_mean missing for material {material}")
                ip_ea_vc_diff = ip_ea_diff
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
            ax1.scatter(ip_ea_vc_diff, efficiency, facecolors='none', edgecolors=color, marker='o', s=50)
            # Annotate the hollow point with the number
            ax1.annotate(str(material_number), (ip_ea_vc_diff, efficiency), textcoords="offset points",
                         xytext=(5, 5), ha='left', fontsize=8, fontstyle='italic')

# Add labels and title for plot (a)
ax1.set_xlabel('IP - EA + VC [eV]')
ax1.set_ylabel(r'Ionization Fraction  $\eta_{\mathrm{sim}}$')

ax1.set_ylim([0.0, 1.0])

# Add a legend for plot (a)
handles, labels = ax1.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))  # Remove duplicate labels
ax1.legend(unique_labels.values(), unique_labels.keys(), loc='lower left')


def central_difference_full(x, y):
    """
    Compute the derivative using a central difference method for all points,
    and return both the derivative and the points (x values) where the derivative was computed.
    Positive values of the derivative will be set to 0 to filter out noise.
    """
    # Convert x and y to NumPy arrays
    x = np.asarray(x)
    y = np.asarray(y)

    # Ensure x and y have the same length
    if len(x) != len(y):
        min_len = min(len(x), len(y))
        x = x[:min_len]
        y = y[:min_len]

    dydx = np.zeros_like(y)
    # Central difference for internal points
    dydx[1:-1] = (y[2:] - y[:-2]) / (x[2:] - x[:-2])
    # Forward difference for the first point
    dydx[0] = (y[1] - y[0]) / (x[1] - x[0])
    # Backward difference for the last point
    dydx[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])

    # Filter out positive values (set them to zero or ignore them)
    dydx[dydx > 0] = 0

    # Return both the derivative and the points (x values)
    return dydx, x


# ---------------------------------------------------
# Right plot (b): Derivative of IP - EA + VC vs Ionization using central difference method
# ---------------------------------------------------
for i, df in enumerate(dataframes):
    # Ensure there are no NaN or misaligned data points
    df = df.dropna(subset=['IP_EA_VC_diff', 'ionization']).reset_index(drop=True)

    # Extract x and y, converting to NumPy arrays
    x = (df['ionization'] * 100).values  # Multiply by 100 to convert to percentage
    y = df['IP_EA_VC_diff'].values

    # Ensure x and y have the same length
    if len(x) != len(y):
        min_len = min(len(x), len(y))
        x = x[:min_len]
        y = y[:min_len]

    # Calculate the derivative using central difference, with filtering
    dydx, x_eval = central_difference_full(x, y)

    # If kcal/mol is used for y-axis, apply the conversion factor
    if use_kcal_per_mol_y_axis:
        dydx *= eV_to_kcal_per_mol  # Convert to kcal/mol

    # Plot the derivative using evaluated points (x values)
    ax2.plot(df['IP_EA_VC_diff'], dydx, color=colors(i), label=material_names[i], linestyle='-', marker='')

# Add labels and title for plot (b)
y_label_unit = 'kcal/mol' if use_kcal_per_mol_y_axis else 'eV'
ax2.set_xlabel('IP - EA + VC [eV]')  # x-axis remains in eV
ax2.set_ylabel(f'd(IP - EA + VC)/d($\eta_{{\mathrm{{sim}}}}$) [{y_label_unit}/%]')

# Add horizontal line at -1 with label
ax2.axhline(y=-1, color='gray', linestyle='--')
ax2.annotate('-1 [kcal/mol] / %', xy=(0.05, -1), xytext=(-0.55, -0.95),
             textcoords='data', color='gray', fontsize=8)

# Add horizontal line at -0.1 with label
ax2.axhline(y=-0.1, color='gray', linestyle='--')
ax2.annotate('-0.1 [kcal/mol] / %', xy=(0.05, -0.1), xytext=(-0.55, -0.05),
             textcoords='data', color='gray', fontsize=8)

# **Add vertical line at IP - EA + VC = 0.0**
ax2.axvline(x=0.0, color='black', linestyle='--')
ax2.annotate('IP - EA + VC = 0', xy=(0.0, ax2.get_ylim()[0]), xytext=(0.5, -1.4),
             textcoords='data', color='black', fontsize=8, rotation=90, verticalalignment='bottom')

# Add a legend for plot (b)
handles, labels = ax2.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))  # Remove duplicate labels
ax2.legend(unique_labels.values(), unique_labels.keys(), loc='lower left')

# Adjust y-limits as necessary to reflect smoother behavior
ax2.set_ylim([-1.5, 0])

# Adjust layout to add the labels (a) and (b)
ax1.text(-0.15, 1.05, "a", transform=ax1.transAxes, fontsize=12, fontweight='bold')
ax2.text(-0.15, 1.05, "b", transform=ax2.transAxes, fontsize=12, fontweight='bold')

# Adjust the layout to make sure everything fits nicely
plt.tight_layout()

# Save the full figure as both PNG and PDF
plot_png = os.path.join(output_dir, 'ionization_derivative_plots_inv.png')
plot_pdf = os.path.join(output_dir, 'ionization_derivative_plots_inv.pdf')

plt.savefig(plot_png, dpi=300)  # Save as PNG
plt.savefig(plot_pdf)  # Save as PDF

# Show the full figure
plt.show()
