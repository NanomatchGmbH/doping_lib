import yaml
from matplotlib import pyplot as plt

lib_file = "lib_updated.yaml"

with open(lib_file) as fid:
    lib = yaml.load(fid, Loader=yaml.CLoader)

offsets = []
zero_or_one = []
particular_values = []
particular_offsets = []
names = []  # To store names for annotations

for material in lib:
    if 'IP_sim' in material and 'EA_sim' in material:
        material_name = material['name']
        names.append(material_name)
        print(material_name)

        offset = material['IP_sim'] - material['EA_sim']
        material['offset'] = offset
        print(offset)
        offsets.append(offset)

        doping_works = material['doping']['works']
        print(doping_works)
        zero_or_one.append(0.0 if not doping_works else 1.0)

        eff_dict = material['doping']['efficiency']['data']
        if isinstance(eff_dict, dict):
            efficiencies = list(eff_dict.values())
            particular_values.extend(efficiencies)
            list_size = len(efficiencies)
            offsets_per_efficiency = [offset] * list_size
            particular_offsets.extend(offsets_per_efficiency)

# Set plot size for better visibility in presentations
plt.figure(figsize=(10, 6))

plt.plot(offsets, zero_or_one, 'o', label="Yes or No")
plt.plot(particular_offsets, particular_values, '*', label="Value")

# Annotating the plot
for i, name in enumerate(names):
    plt.annotate(name, (offsets[i], zero_or_one[i]), fontsize=8, alpha=0.7, rotation=90)

# Enhance labels and title
plt.xlabel("Offset $E_{off}$, eV", fontsize=14)
plt.ylabel("Doping Efficiency", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title("Doping Efficiency vs Offset", fontsize=16)

plt.legend()

# Save the plot with high resolution
plt.savefig("doping_efficiency_plot.png", dpi=300)

plt.show()
