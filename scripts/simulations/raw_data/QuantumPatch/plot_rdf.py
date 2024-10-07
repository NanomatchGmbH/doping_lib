import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# General Formatting for All Plots
mpl.rcParams['font.family'] = 'Arial'  # Use Arial font
mpl.rcParams['font.size'] = 7  # Set font size to 7 pt
mpl.rcParams['axes.linewidth'] = 0.5  # Set axes line width
mpl.rcParams['pdf.fonttype'] = 42  # Ensure fonts are embedded in PDF
mpl.rcParams['axes.labelsize'] = 7
mpl.rcParams['axes.titlesize'] = 7
mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['legend.fontsize'] = 6

# Define the base directory and initialize dictionaries
base_directory = '../../../../simulations/raw_data/Deposit'
rdf_data = {}
dopant_grouping = {}

# Loop through folders with pattern <host>@<dopant>_<dopingfraction>
for folder in os.listdir(base_directory):
    if '@' in folder and '_' in folder:
        folder_path = os.path.join(base_directory, folder)
        output_file = os.path.join(folder_path, 'output_dict.yml')

        if os.path.isfile(output_file):
            print(f"Processing file: {output_file}")
            with open(output_file, 'r') as file:
                data = yaml.safe_load(file)

            # Extract RDF pairs and organize by dopant group
            host, dopant_fraction = folder.split('@')
            dopant, fraction = dopant_fraction.split('_')

            if dopant not in dopant_grouping:
                dopant_grouping[dopant] = []

            dopant_grouping[dopant].append(folder)

            rdf_entries = data.get('RDF', {})
            for key, rdf in rdf_entries.items():
                if key.count('_') == 1:
                    uuid1, uuid2 = key.split('_')
                    if 'x' in rdf and 'y' in rdf:
                        rdf_x = rdf['x']
                        rdf_y = rdf['y']

                        # Check if RDF data is valid
                        if (isinstance(rdf_x, list) and isinstance(rdf_y, list) and
                                len(rdf_x) == len(rdf_y) and len(rdf_x) > 0 and
                                all(isinstance(i, (int, float)) for i in rdf_x) and
                                all(isinstance(i, (int, float)) for i in rdf_y)):
                            # Store RDF data, calculating mean if needed for cross compounds
                            pair_key = f"{uuid1}_{uuid2}" if uuid1 < uuid2 else f"{uuid2}_{uuid1}"
                            if pair_key not in rdf_data:
                                rdf_data[pair_key] = {'x': rdf_x, 'y': np.array(rdf_y),
                                                      'first_peak': rdf.get('first_peak')}
                            else:
                                # Average the RDF values if both combinations exist
                                rdf_data[pair_key]['y'] = (rdf_data[pair_key]['y'] + np.array(rdf_y)) / 2
                                if rdf.get('first_peak') is not None:
                                    rdf_data[pair_key]['first_peak'] = (rdf_data[pair_key]['first_peak'] + rdf.get(
                                        'first_peak')) / 2
                        else:
                            print(f"Invalid RDF data for key {key} in file {output_file}")
                    else:
                        print(f"Missing 'x' or 'y' in RDF data for key {key} in file {output_file}")

# General plot settings
full_page_width = 7.08  # inches (18 cm)
fig_width = full_page_width  # For full width figure
fig_height = full_page_width * (3 / 4)  # Adjust height as needed

# Number of dopants
num_dopants = len(dopant_grouping)

# Create figure and axes for dopants
fig, axes = plt.subplots(num_dopants, 1, figsize=(fig_width, fig_height), sharex=False)
axes = np.atleast_1d(axes)  # Ensure axes is iterable even if there's only one subplot

# Determine global y-axis limits for cross pairs only
global_max_y = 0
for key, rdf in rdf_data.items():
    if key.count('_') == 1:
        if key.split('_')[0] != key.split('_')[1]:
            global_max_y = max(global_max_y, max(rdf['y']))
y_max = global_max_y + 0.5

for idx, (dopant, folders) in enumerate(dopant_grouping.items()):
    ax = axes[idx]
    print(f"Plotting RDFs for dopant: {dopant}")
    ax.set_title(f'Dopant: {dopant}', fontsize=7)

    valid_plots = False
    plotted_pairs = set()
    for folder in folders:
        folder_path = os.path.join(base_directory, folder)
        output_file = os.path.join(folder_path, 'output_dict.yml')

        if os.path.isfile(output_file):
            print(f"Reading data from: {output_file}")
            with open(output_file, 'r') as file:
                data = yaml.safe_load(file)

            rdf_entries = data.get('RDF', {})
            for key, rdf in rdf_entries.items():
                if key.count('_') == 1:
                    uuid1, uuid2 = key.split('_')
                    if uuid1 != uuid2 and 'x' in rdf and 'y' in rdf:  # Cross-compounds only
                        pair_key = f"{uuid1}_{uuid2}" if uuid1 < uuid2 else f"{uuid2}_{uuid1}"
                        if pair_key not in plotted_pairs and pair_key in rdf_data:
                            rdf_x = rdf_data[pair_key]['x']
                            rdf_y = rdf_data[pair_key]['y']

                            # Find and mark the first peak
                            first_peak = rdf_data[pair_key].get('first_peak')
                            if first_peak is not None:
                                peak_index = rdf_x.index(min(rdf_x, key=lambda x: abs(x - first_peak)))
                                peak_distance = rdf_x[peak_index]
                                peak_value = rdf_y[peak_index]

                                # Plot the RDF
                                print(f"Plotting RDF for {uuid1} <> {uuid2}, Peak at distance: {peak_distance}")
                                ax.plot(rdf_x, rdf_y, label=f'{folder}', linewidth=0.5)
                                ax.scatter([peak_distance], [peak_value], color='red', s=10)
                                ax.text(peak_distance, peak_value, f'{peak_distance:.2f} Å', fontsize=6, color='red',
                                        ha='right')
                                valid_plots = True
                                plotted_pairs.add(pair_key)
                            else:
                                print(f"First peak data missing for {uuid1} <> {uuid2} in file {output_file}")

    if valid_plots:
        ax.set_xlabel('Distance (Å)', fontsize=7)
        ax.set_ylabel('RDF', fontsize=7)
        ax.set_ylim(-0.1, y_max)
        ax.set_xlim(-2, 20)
        ax.legend(fontsize=6, frameon=False)
    else:
        print(f"No valid plots for dopant: {dopant}")

    # Add subplot label
    ax.text(-0.1, 1.05, chr(97 + idx), transform=ax.transAxes, fontsize=12, fontweight='bold', ha='left', va='top')

# Adjust layout to ensure everything fits nicely
plt.tight_layout(pad=0.2, h_pad=0.5)

# Save the figure in high-resolution PNG and PDF formats
plt.savefig('rdf_cross_pairs_advanced_materials.png', dpi=600, bbox_inches='tight')
plt.savefig('rdf_cross_pairs_advanced_materials.pdf', dpi=600, bbox_inches='tight')

# Display the plot
plt.show()