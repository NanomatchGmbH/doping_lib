import argparse
import yaml
import matplotlib.pyplot as plt
import numpy as np

# Constants
e = 1.602e-19  # Elementary charge in coulombs
NA = 6.022e23  # Avogadro's number

def mr_to_mol_percent(mr):
    """Convert molar ratio to mol%."""
    return (mr / (1 + mr)) * 100

def calculate_mobility(sigma, molar_fraction, molar_volume=1):
    """Calculate mobility in cm^2/Vs from given sigma and molar fraction."""
    if molar_fraction == 0:
        return None  # Return None for zero molar fraction to indicate no calculation possible
    x = molar_fraction / 100 * molar_volume  # Assume molar_volume in mol/m^3
    n = NA * x
    mu_m2 = sigma / (n * e)
    mu_cm2 = mu_m2 * 1e4  # Convert from m^2 to cm^2
    return mu_cm2

# Argument parsing
parser = argparse.ArgumentParser(description="Plot conductivity or mobility versus doping concentration.")
parser.add_argument("--mobility", action="store_true", help="Plot mobility instead of conductivity")
args = parser.parse_args()

# Load the YAML data
with open('lib.yaml', 'r') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

# Prepare the plot
fig, ax = plt.subplots()
colormap = plt.cm.get_cmap('tab20', len(data))

# Iterate through each material entry in the YAML data
for index, material in enumerate(data):
    name = material['name']
    if 'conductivity' in material:
        con_data = material['conductivity']['data']

        # Check if conversion from MR to mol% is needed
        if material['conductivity']['units'] == 'MR':
            con_data = {mr_to_mol_percent(float(k)): v for k, v in con_data.items()}

        concentrations = list(con_data.keys())
        values = list(con_data.values())

        # Calculate mobility if the flag is set
        if args.mobility:
            values = [calculate_mobility(sigma, float(conc)) for sigma, conc in zip(values, concentrations)]
            ylabel = 'Mobility (cm$^2$/Vs)'
        else:
            ylabel = 'Conductivity (S cm$^{-1}$)'

        # Use the colormap to assign a color
        color = colormap(index)
        ax.plot(concentrations, values, marker='o', linestyle='-', label=name, color=color)

# Set log scale for both axes
ax.set_xscale('log')
ax.set_yscale('log')
plt.xlim([1E-1, 100])

# Configure the plot
ax.set_xlabel('Doping Concentration (mol%)')
ax.set_ylabel(ylabel)
ax.set_title(f'Log-Scale {ylabel} vs. Doping Concentration')
ax.legend(fontsize='small')
plt.grid(True, which="both", ls="--")

# Show the plot
plt.show()

