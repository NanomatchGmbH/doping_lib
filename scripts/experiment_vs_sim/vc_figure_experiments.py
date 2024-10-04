import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# General Formatting for All Plots
mpl.rcParams['font.family'] = 'Arial'  # Use Arial font
mpl.rcParams['font.size'] = 7          # Set font size to 7 pt
mpl.rcParams['axes.linewidth'] = 0.5   # Set axes line width
mpl.rcParams['pdf.fonttype'] = 42      # Ensure fonts are embedded in PDF
mpl.rcParams['axes.labelsize'] = 7
mpl.rcParams['axes.titlesize'] = 7
mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['legend.fontsize'] = 6

# Figure size in inches
full_page_width = 7.08  # inches (18 cm)
fig_width = full_page_width
fig_height = full_page_width * (3/4)

# Create figure and axes
fig, axes = plt.subplots(2, 2, figsize=(fig_width, 6))
axes = axes.flatten()

# --- Combined Plot a ---
# Use axes[0]

# Read data from the CSV file
rdf_peak_df = pd.read_csv('../../simulations/summary/Deposit/first_rdf_peak.csv')
rdf_peak_df['clean_material'] = rdf_peak_df['material'].apply(lambda x: x.split('_')[0])

# Read VC data from merged YAML file
vc_data = pd.read_csv('../../simulations/summary/Deposit/VC_at_first_rdf_peak.csv')
vc_data['clean_material'] = vc_data['material'].apply(lambda x: x.split('_')[0])

# Sort the DataFrame by 'first_rdf_peak' in ascending order
rdf_peak_df_sorted = rdf_peak_df.sort_values(by='first_rdf_peak')

# Plotting on axes[0]
ax1 = axes[0]  # Primary y-axis
ax2 = ax1.twinx()  # Secondary y-axis

# Bar plot for the First RDF Peak
rdf_bar = ax1.bar(rdf_peak_df_sorted['clean_material'], rdf_peak_df_sorted['first_rdf_peak'], 
                  color='skyblue', edgecolor='black', label='First RDF Peak (Å)')

# Match VC data to rdf_peak_df_sorted order
vc_data_sorted = vc_data.set_index('clean_material').loc[rdf_peak_df_sorted['clean_material']].reset_index()

# Plotting VC at the First RDF Peak on the secondary y-axis
vc_line = ax2.plot(vc_data_sorted['clean_material'], vc_data_sorted['VC_mean'], 
                   color='darkorange', linestyle='-', marker='o', markersize=3, label='$V_C$ at First RDF Peak (eV)')

# Customizing the plot
ax1.set_xlabel('Material')
ax1.set_ylabel('First RDF Peak (Å)', color='skyblue')
ax2.set_ylabel('$V_C$ at First RDF Peak (eV)', color='darkorange')

# Rotate x-tick labels for readability
ax1.set_xticklabels(rdf_peak_df_sorted['clean_material'], rotation=45, ha='right')

# Set title for combined plot
ax1.set_title('a', fontsize=10, fontweight='bold', loc='left')

# Adding legends for both y-axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper right', frameon=False)

# Adjust other y-axes properties to make the plot more readable
ax1.tick_params(axis='y', colors='skyblue')
ax2.tick_params(axis='y', colors='darkorange')

# --- Plot b (unchanged) ---
# Continue with the rest of your original plotting code for b, c, d

# Plot b is axes[1]
# Plot c (which is now merged with a) is removed
# Plot d is axes[3]

# Adjust layout for tightness
plt.tight_layout(pad=0.2)

# Save and display the plot
plt.savefig('combined_plot_a_c.png', dpi=300)
plt.show()
