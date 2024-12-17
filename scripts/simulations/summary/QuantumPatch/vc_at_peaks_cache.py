import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import re  # Import regular expressions module
import yaml

# Path to the merged YAML file
# yaml_file_path = 'merged_vc_data.yaml'
yaml_file_path = '../../../../simulations/summary/QuantumPatch/merged_vc_data.yaml'

# Read the CSV file containing first RDF peak distances
rdf_peak_file = '../../../../simulations/summary/Deposit/first_rdf_peak.csv'

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

mpl.rcParams['axes.linewidth'] = 0.5   # Set axes line width
mpl.rcParams['pdf.fonttype'] = 42      # Ensure fonts are embedded in PDF


# Read the first_rdf_peak data
rdf_peak_df = pd.read_csv(rdf_peak_file)

# Modify material names by removing everything from '_' onwards
def clean_material_name(name):
    return name.split('_')[0]

rdf_peak_df['clean_material'] = rdf_peak_df['material'].apply(clean_material_name)
rdf_peak_df.set_index('material', inplace=True)

# List of materials (folders) to process
materials = rdf_peak_df.index.tolist()


# Check if the merged YAML file exists
if not os.path.isfile(yaml_file_path):
    raise FileNotFoundError(f"{yaml_file_path} not found. Please generate the YAML file first.")

# Load the merged YAML file
with open(yaml_file_path, 'r') as yaml_file:
    merged_data = yaml.load(yaml_file, Loader=yaml.SafeLoader)

# Initialize a list to store results
results = []

# Process each material
for material in materials:
    first_rdf_peak = rdf_peak_df.loc[material, 'first_rdf_peak']
    clean_name = rdf_peak_df.loc[material, 'clean_material']

    # Use the material name to retrieve data from YAML instead of CSV
    if material in merged_data:
        data = pd.DataFrame({
            'dimer_comdist': merged_data[material]['inverse_distance'],
            'VC_corrected': merged_data[material]['VC_corrected']
        })
        data['dimer_comdist'] = 1 / data['dimer_comdist']  # Convert inverse distance back to distance

        # Find the indices of the data points just below and just above the first_rdf_peak
        distances = data['dimer_comdist']
        differences = distances - first_rdf_peak

        # Get indices where difference is negative (below the peak) and positive (above the peak)
        differences_below = differences[differences <= 0]
        differences_above = differences[differences > 0]

        # Initialize vc_below and vc_above
        vc_below = None
        vc_above = None

        # Check if there are data points above the peak
        if not differences_above.empty:
            idx_above = differences_above.idxmin()
            vc_above = data.loc[idx_above, 'VC_corrected']

            # Use vc_above as VC_mean
            vc_mean = vc_above

            # Optionally average with below if available
            if not differences_below.empty:
                idx_below = differences_below.idxmax()
                vc_below = data.loc[idx_below, 'VC_corrected']
                # Compute the mean VC_corrected value
                vc_mean = (vc_below + vc_above) / 2
            # Else, vc_mean is vc_above

        elif not differences_below.empty:
            # No data above, but data below exists
            idx_below = differences_below.idxmax()
            vc_below = data.loc[idx_below, 'VC_corrected']
            vc_mean = vc_below
        else:
            # No data above or below; take the closest point overall
            differences_abs = differences.abs()
            idx_closest = differences_abs.idxmin()
            vc_mean = data.loc[idx_closest, 'VC_corrected']
            print(f"No data above or below the first RDF peak for {material}. Using closest data point.")

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

# Remove duplicates in case multiple entries have the same clean material name
results_df = results_df.groupby('material', as_index=False).mean()

# Save the results to a CSV file
results_df.to_csv('VC_at_first_rdf_peak_cleaned.csv', index=False)

# Plot the VC_mean values for each material
# Sort the DataFrame by VC_mean for better visualization
results_df.sort_values(by='VC_mean', inplace=True)

# Create the plot
plt.figure(figsize=(3.54, 3))
plt.barh(results_df['material'], results_df['VC_mean'], color='skyblue')
plt.xlabel('$V_C$ at First RDF Peak (eV)', fontsize=12)
plt.ylabel('Material', fontsize=12)
plt.xlim([-0.9, -.6])
plt.tight_layout()
plt.savefig('VC_at_first_rdf_peak_cleaned.png', dpi=600)
plt.savefig('VC_at_first_rdf_peak_cleaned.pdf', dpi=600)
plt.show()

