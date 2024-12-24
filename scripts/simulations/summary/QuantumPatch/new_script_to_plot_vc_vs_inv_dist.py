import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml

# List of materials to plot
materials_list = ['TCTA@CN6-CP_0.26', 'TCTA@F6TCNNQ_0.11', 'MeO-TPD@F4TCNQ_0.07']  # Add more materials as needed

# Load the merged YAML data (replace with actual path)
yaml_file_path = '../../../../simulations/summary/QuantumPatch/merged_vc_data.yaml'
with open(yaml_file_path, 'r') as yaml_file:
    merged_data = yaml.safe_load(yaml_file)

# Load the RDF peak data
rdf_peak_df = pd.read_csv('../../../../simulations/summary/Deposit/first_rdf_peak.csv')
rdf_peak_df['material_clean'] = rdf_peak_df['material'].apply(lambda x: x.split('_')[0])
rdf_peak_df.set_index('material_clean', inplace=True)

# Create the plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Iterate over each material
for material_name in materials_list:
    # Check if the material exists in the data
    if material_name in merged_data:
        material_data = merged_data[material_name]
    else:
        print(f"Material {material_name} not found in the data.")
        continue

    # Extract inverse distance and VC corrected data
    inverse_distance = np.array(material_data['inverse_distance'])
    vc_corrected = np.array(material_data['VC_corrected'])

    # Sort the data by inverse distance
    sorted_indices = np.argsort(inverse_distance)
    inverse_distance_sorted = inverse_distance[sorted_indices]
    vc_corrected_sorted = vc_corrected[sorted_indices]

    # Convert inverse distance to direct distance
    direct_distance_sorted = 1 / inverse_distance_sorted

    # Find the first RDF peak and VC at that peak for the specific material
    first_rdf_peak = None
    vc_at_first_rdf_peak = None

    # Attempt to match the material name more flexibly
    clean_material_name = material_name.split('_')[0]  # Use only the host name for matching
    matched_materials = rdf_peak_df.index[rdf_peak_df.index.str.contains(clean_material_name)]

    if not matched_materials.empty:
        first_rdf_peak = rdf_peak_df.loc[matched_materials[0], 'first_rdf_peak']

        # Find the VC at the first RDF peak by finding the closest inverse distance
        data_df = pd.DataFrame({
            'direct_distance': direct_distance_sorted,  # Use direct distance now
            'VC_corrected': vc_corrected_sorted
        })
        idx_closest = (data_df['direct_distance'] - first_rdf_peak).abs().idxmin()
        vc_at_first_rdf_peak = data_df.loc[idx_closest, 'VC_corrected']
    else:
        print(f"No matching RDF peak data for {material_name}.")
        continue

    # --- Plotting both panels a and b ---

    # --- Panel a: VC vs. Inverse Distance ---
    ax1.plot(inverse_distance_sorted, vc_corrected_sorted, label=f'{material_name}', marker='o', linestyle='--')
    ax1.scatter(1 / first_rdf_peak, vc_at_first_rdf_peak, color='red', marker='*', s=150)

    # --- Panel b: VC vs. Direct Distance ---
    ax2.plot(direct_distance_sorted, vc_corrected_sorted, label=f'{material_name}', marker='o', linestyle='--')
    ax2.scatter(first_rdf_peak, vc_at_first_rdf_peak, color='red', marker='*', s=150)

# Customize Panel a
ax1.set_xlabel('Inverse Center of Mass Distance (1/Å)')
ax1.set_ylabel('$V_C$ (eV)')
ax1.set_title('VC vs Inverse Distance')
ax1.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Customize Panel b
ax2.set_xlabel('Direct Distance (Å)')
ax2.set_ylabel('$V_C$ (eV)')
ax2.set_title('VC vs Direct Distance')
ax2.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Add legend to both panels
ax1.legend(loc='upper right')
ax2.legend(loc='upper right')

# Adjust layout for better spacing
plt.tight_layout()
plt.savefig(f'vc_vs_inverse_and_direct_distance_multiple_materials.png', dpi=300)
plt.show()
