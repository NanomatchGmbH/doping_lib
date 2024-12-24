import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# scale factor for parametric conductivity
SCALE = 0.2E3

# Load parametric conductivity
data = pd.read_csv("../parametric_conductivity/all_simulations_conductivity.csv")
# Calculate standard error from standard deviation

# SCALE
data['sigma [S/cm]'] = SCALE * data['sigma [S/cm]']
data['std_err'] = data['sigma_std [S/cm]'] / np.sqrt(31.0)
data['IP - EA [eV]'] = 4.0 - data['simulation']
data['onset IP - EA [eV]'] = 4.0 - data['simulation'] - 0.4

# Load simulated IP-EA vs exper. conductivity
extra_data = pd.read_csv("../exper_conductivity_vs_simulated_ip_ea/data.csv")

# Set up the plotting environment
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Use tab10 colormap for consistent styling
tab10 = plt.cm.get_cmap('tab10')

# Choose colors from tab10: blue and red
blue_color = tab10(0)  # default "tab10" blue
red_color = tab10(3)   # default "tab10" red



# plot Fermi function -->
x_values = np.linspace(-0.5, 1.5, 100)
def Fermi(x_values):
    return 10.0 / (1 + np.exp((x_values - 0.7) / .025))
y_values = Fermi(x_values)
plt.plot(x_values, y_values, '--', color='black', alpha=0.6,
         label=r'$C \cdot \exp\left(E_{CT}/k_B T\right)$ vs (IP - EA)')
# <-- plot Fermi function



# Plot main data with log scale for the y-axis
plot_main = sns.lineplot(x='IP - EA [eV]', y='sigma [S/cm]', data=data, marker=None, label=r'$\sigma_{sim}$ vs (IP - EA)',
                         color=red_color)
# plot_main_1 = sns.lineplot(x='onset IP - EA [eV]', y='sigma [S/cm]', data=data, marker=None, label='kMC simulations (5 mol%) onset',
#                          color='blue')
# plt.errorbar(data['IP - EA [eV]'], data['sigma [S/cm]'], xerr=data['std_err'], fmt='o', capsize=5, color='blue')

# Plot extra data

plt.scatter(extra_data['IP - EA (eV)'], extra_data['Conductivity [S/cm]'], color=red_color, marker='o', label='$\sigma_{exp}$ vs (IP - EA)')
plt.scatter(extra_data['exper. IP - EA (eV)'], extra_data['Conductivity [S/cm]'], color=blue_color, marker='x', label='$\sigma_{exp}$ vs (IP$_{onset}$ - EA$_{onset}$)')




# Set the y-axis to logarithmic scale and adjust limits
plt.yscale('log')
max_value = max(data['sigma [S/cm]'].max(), extra_data['Conductivity [S/cm]'].max())
plt.ylim(max_value / 1e6, max_value * 10)
plt.xlim(-1.0, 1.5)

# Adding labels and title
plt.xlabel('IP - EA [eV]')
plt.ylabel('Conductivity (S/cm)')
# plt.title('Conductivity vs IP-EA [eV]')

# Add legend
plt.legend()

# Add a second x-axis for IP_onset - EA_onset
# ax = plt.gca()
# ax2 = ax.twiny()
# ax2.set_xlabel('Experimental IP$_{onset}$ - EA$_{onset}$ [eV]')

# Remove labels and ticks on the second axis
# ax2.set_xlabel('')
# ax2.set_xticks([])

# The "onset" axis is shifted by 0.4 relative to IP - EA
# We simply adjust the new axis limits by subtracting 0.4 from the original:
# orig_xlim = ax.get_xlim()
# ax2.set_xlim(orig_xlim[0] - 0.4, orig_xlim[1] - 0.4)

# Show the plot
# plt.show()
plt.savefig("Figure5.png", dpi=600)
plt.savefig("Figure5.pdf")
plt.close()
