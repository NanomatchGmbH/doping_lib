import argparse
import yaml
import matplotlib.pyplot as plt
import numpy as np

# Constants
e = 1.602e-19  # Elementary charge in coulombs
NA = 6.022e23  # Avogadro's number

markers = ['o', 's', '^', '>', '<', 'v', 'p', 'h', '+', 'x', '*', 'D']


def get_color(value, max_value):
    return plt.cm.viridis(value / max_value)


# Function to get a color based on value
def get_color(value, max_value):
    return plt.cm.viridis(value / max_value)


# Function to get marker size based on value
def get_marker_size(value):
    return 20 + 10 * (value / max(value))


def filter_by_concentration_range(concentrations, values, min_conc, max_conc):
    """Filter concentrations and corresponding values within a specified range."""
    filtered_concentrations = []
    filtered_values = []
    for conc, val in zip(concentrations, values):
        if min_conc <= float(conc) <= max_conc:
            filtered_concentrations.append(conc)
            filtered_values.append(val)
    return filtered_concentrations, filtered_values


def get_intrinsic_mobility(mobility_data):
    """Create a dictionary mapping host materials to their intrinsic mobility."""
    intrinsic_mobility = {}
    for host, entries in mobility_data.items():
        # Attempt to find a TOF method entry, otherwise use the first entry available
        tof_mobility = next((entry['data'] for entry in entries if entry.get('method', '').lower() == 'tof'), None)
        if tof_mobility is not None:
            intrinsic_mobility[host] = tof_mobility
        elif entries:
            intrinsic_mobility[host] = entries[0]['data']
    return intrinsic_mobility


# Load the YAML data for intrinsic mobilities
with open('mobility.yaml', 'r') as file:
    mobility_data = yaml.load(file, Loader=yaml.FullLoader)

# Retrieve intrinsic mobility mapping
intrinsic_mobility = get_intrinsic_mobility(mobility_data)

# Print the intrinsic mobilities for verification
for host, mobility in intrinsic_mobility.items():
    print(f"Host: {host}, Intrinsic Mobility: {mobility}")


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
parser.add_argument("--normalized_mobility", action="store_true",
                    help="Plot normalized mobility instead of conductivity")
args = parser.parse_args()

# Load the YAML data
with open('lib.yaml', 'r') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

# Prepare the first plot (conductivity / mobility)
fig, ax = plt.subplots()
colormap = plt.cm.get_cmap('tab20', len(data))

# Initialize the second plot for IP minus EA if normalized mobility is plotted
if args.normalized_mobility:
    fig1, ax1 = plt.subplots()
    colormap1 = plt.cm.get_cmap('tab20b', len(data))  # Different colormap for distinction
    colormap1 = plt.cm.get_cmap('tab20b', len(data))  # Different colormap for distinction

# Iterate through each material entry in the YAML data
for index, material in enumerate(data):
    name = material['name']
    color = colormap(index)  # Define color here to use in both plots
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
        # Calculate normalized mobility
        elif args.normalized_mobility:
            host = material['host']
            dopant = material['dopant']
            if host == 'ZnPc' or host == 'Pc':
                continue
            mu_i = float(intrinsic_mobility[host])
            ip = material['IP']['value']
            ea = material['EA']['value']
            ip_minus_ea = ip - ea
            values = [(calculate_mobility(sigma, float(conc)) / mu_i if calculate_mobility(sigma, float(
                conc)) is not None else None) for sigma, conc in zip(values, concentrations)]

            # Specify the concentration range you are interested in
            min_concentration = 1.0  # minimum doping concentration in mol%
            max_concentration = 10.0  # maximum doping concentration in mol%
            filtered_concentrations, filtered_values = filter_by_concentration_range(concentrations, values,
                                                                                     min_concentration,
                                                                                     max_concentration)

            marker = markers[index % len(markers)]  # Cycle through markers

            # Plot normalized mobility vs doping concentration
            ax.plot(filtered_concentrations, filtered_values, marker='o', linestyle='-', label=name, color=color)
            ax1.plot([ip_minus_ea] * len(filtered_values), filtered_values, marker=marker, linestyle='-', label=name,
                     color=color)

            print(f"{ip=}")
            print(f"{ea=}")
            print(f"{[ip_minus_ea] * len(values)=}")
            print(f"{values=}")

            ylabel = 'Mobility Normalized'
            ylabel1 = 'Normalized Mobility vs. IP-EA'

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

# Configuration for the second plot
if args.normalized_mobility:
    ax1.set_xlabel('IP - EA (eV)')
    ax1.set_yscale('log')
    ax1.set_ylabel(ylabel1)
    ax1.set_title('Normalized Mobility vs. IP - EA')
    ax1.legend(fontsize='small')
    ax1.set_xlim([-.6, .6])
    ax1.grid(True, which="both", ls="--")

# Show the plot(s)
plt.show()
