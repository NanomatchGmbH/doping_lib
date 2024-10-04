import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml

# Sample data for one specific material (replace 'material_name' with actual name)
material_name = 'TCTA@CN6-CP_0.26'  # Replace this with the specific material you're interested in

# Load the merged YAML data (replace with actual path)
yaml_file_path = '../../../../simulations/summary/QuantumPatch/merged_vc_data.yaml'
with open(yaml_file_path, 'r') as yaml_file:
    merged_data = yaml.safe_load(yaml_file)

# Check if the material exists in the data
if material_name in merged_data:
    material_data = merged_data[material_name]
else:
    print(f"Material {material_name} not found in the data.")
    exit()

# Extract inverse distance and VC corrected data
inverse_distance = np.array(material_data['inverse_distance'])
vc_corrected = np.array(material_data['VC_corrected'])

# Load the RDF peak data
rdf_peak_df = pd.read_csv('../../../../simulations/summary/Deposit/first_rdf_peak.csv')
rdf_peak_df['material_clean'] = rdf_peak_df['material'].apply(lambda x: x.split('_')[0])
rdf_peak_df.set_index('material', inplace=True)

# Find the first RDF peak and VC at that peak for the specific material
first_rdf_peak = None
vc_at_first_rdf_peak = None

# Find the RDF peak for the material (without the doping info)
clean_material_name = material_name.split('_')[0]
if clean_material_name in rdf_peak_df['material_clean'].values:
    first_rdf_peak = rdf_peak_df.loc[material_name.split('_')[0], 'first_rdf_peak']

    # Find the VC at the first RDF peak by finding the closest inverse distance
    data_df = pd.DataFrame({
        'dimer_comdist': 1 / inverse_distance,  # Convert inverse distance back to distance
        'VC_corrected': vc_corrected
    })
    idx_closest = (data_df['dimer_comdist'] - first_rdf_peak).abs().idxmin()
    vc_at_first_rdf_peak = data_df.loc[idx_closest, 'VC_corrected']
else:
    print(f"RDF peak data for {material_name} not found.")
    exit()

# --- Plotting ---
plt.figure(figsize=(6, 4))

# Plot VC vs. Inverse Distance
plt.plot(inverse_distance, vc_corrected, label=f'{material_name}', color='blue', marker='o', linestyle='--')

# Highlight the RDF peak and VC at that peak
plt.scatter(1 / first_rdf_peak, vc_at_first_rdf_peak, color='red', marker='*', s=150, label='RDF Peak')

# Customize the plot
plt.xlabel('Inverse Center of Mass Distance (1/Å)')
plt.ylabel('$V_C$ (eV)')
plt.title(f'$V_C$ vs Inverse Distance for {material_name}')
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Save the figure
plt.tight_layout()
plt.savefig(f'vc_vs_inverse_distance_{material_name}.png', dpi=300)
plt.show()
