import pandas as pd
import matplotlib.pyplot as plt

# Read data from the CSV file
df = pd.read_csv('../../../../simulations/summary/Deposit/first_rdf_peak.csv')

# Remove doping information by splitting at '_' and keeping the part before it
df['material_clean'] = df['material'].apply(lambda x: x.split('_')[0])

# Sort the DataFrame by 'first_rdf_peak' in ascending order
df_sorted = df.sort_values(by='first_rdf_peak')

# Plotting
plt.figure(figsize=(8, 4))  # Adjust figure size for half-page width

# Create the bar plot
plt.bar(df_sorted['material_clean'], df_sorted['first_rdf_peak'], color='skyblue', edgecolor='black')

# Customizing the plot for publication style
plt.xlabel('Material', fontsize=14)
plt.ylabel('First RDF Peak (Å)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels 45 degrees
plt.yticks(fontsize=12)
plt.ylim(4, )
plt.title('First RDF Peak vs. Material', fontsize=16)
plt.tight_layout()

# Save the plot with high resolution
plt.savefig('../../../../simulations/summary/Deposit/rdf_peak_vs_material_sorted.png', dpi=300, bbox_inches='tight')
plt.show()
