import os
import yaml
import numpy as np
import matplotlib.pyplot as plt

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

                        # Debugging: Print the lengths and content of x and y
                        print(f"Key: {key}, Length of x: {len(rdf_x)}, Length of y: {len(rdf_y)}")
                        print(f"Full x: {rdf_x}")
                        print(f"Full y: {rdf_y}")

                        # Check if RDF data is valid
                        if (isinstance(rdf_x, list) and isinstance(rdf_y, list) and
                                len(rdf_x) == len(rdf_y) and len(rdf_x) > 0 and
                                all(isinstance(i, (int, float)) for i in rdf_x) and
                                all(isinstance(i, (int, float)) for i in rdf_y)):
                            # Store RDF data, calculating mean if needed for cross compounds
                            pair_key = f"{uuid1}_{uuid2}" if uuid1 < uuid2 else f"{uuid2}_{uuid1}"
                            if pair_key not in rdf_data:
                                rdf_data[pair_key] = {'x': rdf_x, 'y': np.array(rdf_y)}
                            else:
                                # Average the RDF values if both combinations exist
                                rdf_data[pair_key]['y'] = (rdf_data[pair_key]['y'] + np.array(rdf_y)) / 2
                        else:
                            print(f"Invalid RDF data for key {key} in file {output_file}")
                    else:
                        print(f"Missing 'x' or 'y' in RDF data for key {key} in file {output_file}")

# Plot RDFs grouped by dopants
for dopant, folders in dopant_grouping.items():
    print(f"Plotting RDFs for dopant: {dopant}")
    plt.figure(figsize=(15, 10))
    plt.suptitle(f'RDF Cross-pairs for Dopant: {dopant}', fontsize=16)

    valid_plots = False
    for idx, folder in enumerate(folders):
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
                        if pair_key in rdf_data:
                            rdf_x = rdf_data[pair_key]['x']
                            rdf_y = rdf_data[pair_key]['y']

                            # Find and mark the first peak
                            first_peak = rdf.get('first_peak', None)
                            if first_peak is not None:
                                peak_index = rdf_x.index(min(rdf_x, key=lambda x: abs(x - first_peak)))
                                peak_distance = rdf_x[peak_index]
                                peak_value = rdf_y[peak_index]

                                # Plot the RDF
                                print(f"Plotting RDF for {uuid1} <> {uuid2}, Peak at distance: {peak_distance}")
                                plt.subplot(len(folders) // 2 + 1, 2, idx + 1)
                                plt.plot(rdf_x, rdf_y, label=f'{uuid1} <> {uuid2}')
                                plt.scatter([peak_distance], [peak_value], color='red')
                                plt.axvline(x=peak_distance, linestyle='--', color='gray',
                                            label=f'Peak at {peak_distance:.2f}')
                                plt.xlabel('Distance')
                                plt.ylabel('RDF')
                                plt.title(f'RDF for {uuid1} <> {uuid2}')
                                plt.legend()
                                valid_plots = True
                            else:
                                print(f"First peak data missing for {uuid1} <> {uuid2} in file {output_file}")

    if valid_plots:
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()
    else:
        print(f"No valid plots for dopant: {dopant}")