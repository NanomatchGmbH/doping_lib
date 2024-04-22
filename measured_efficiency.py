"""
This script extracts all doped materials where efficiency was measured, i.e., extracted from the experimental data.
In some cases, I have evaluated it using ratio in a J-V curve.
It also saves the names of materials and doping efficiencies as csv file.
"""

import pandas as pd
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

LIB_NAME = 'lib.yaml'

exclude_hosts = ['P3HT']
exclude_dopants = ['C60F48', 'C60F36']


def read_yaml(yaml_name):
    with open(yaml_name, 'r') as fid:
        return yaml.load(fid, Loader=yaml.CLoader)


yaml_data = read_yaml(LIB_NAME)

materials_counter = 0

filtered_materials = []

list_of_dicts = []
df_has_value = pd.DataFrame(columns=['name', 'IP', 'EA', 'offset', 'efficiency', 'doping'])

for material in yaml_data:
    dopant_ionization_rate = material['doping']['efficiency']['data']
    # print(material)
    if dopant_ionization_rate and material['host'] not in exclude_hosts and material['dopant'] not in exclude_dopants:
        if list(dopant_ionization_rate.values())[0] is not None:
            # if list(dopant_ionization_rate.values())[0] != 1.0:
                tmp_dict = {}
                print(material['name'])
                materials_counter += 1
                doping_units = material['concentration']['units']
                if doping_units == 'mol%':
                    print(dopant_ionization_rate, doping_units)
                elif doping_units == 'MR':
                    print(dopant_ionization_rate, doping_units)
                    print("or")
                    print(list(dopant_ionization_rate.keys())[0] / (1 + list(dopant_ionization_rate.keys())[0]), "mol%")
                else:
                    print(f"I do not know units {doping_units}")
                filtered_materials.append(material)
                tmp_dict['name'] = material['name']
                tmp_dict['IP'] = material['IP']['value']
                tmp_dict['EA'] = material['EA']['value']
                tmp_dict['offset'] = tmp_dict['IP'] - tmp_dict['EA']
                print(tmp_dict['offset'])
                tmp_dict['efficiency'] = list(dopant_ionization_rate.values())[0]
                tmp_dict['doping'] = list(dopant_ionization_rate.keys())[0]
                list_of_dicts.append(tmp_dict)

# add all materials for which the doping does not work to the materials with zero efficiencies
print("Dopants which zero efficiencies: ")
for material in yaml_data:
    dopant_ionization_rate = material['doping']['efficiency']['data']
    if not dopant_ionization_rate and material['host'] not in exclude_hosts and material['dopant'] not in exclude_dopants and material['doping']['works'] == False:
        tmp_dict = {}
        print(material['name'])
        materials_counter += 1
        # print(dopant_ionization_rate)
        filtered_materials.append(material)
        tmp_dict['name'] = material['name']
        tmp_dict['IP'] = material['IP']['value']
        tmp_dict['EA'] = material['EA']['value']
        tmp_dict['offset'] = tmp_dict['IP'] - tmp_dict['EA']
        print(tmp_dict['offset'])
        tmp_dict['efficiency'] = 0.0
        tmp_dict['doping'] = None
        list_of_dicts.append(tmp_dict)

df_has_value = pd.DataFrame(list_of_dicts)

print(f"Number of materials excluding hosts {exclude_hosts} and dopants {exclude_dopants} is: {materials_counter}")

print([filtered_material['name'] for filtered_material in filtered_materials])


#  PLOT all materials which efficiency is evaluated quantitatively

# Assuming df_has_value is your DataFrame

# Create the scatter plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
scatter_plot = sns.scatterplot(data=df_has_value, x='offset', y='efficiency', s=100)  # s is the size of points

# Annotate each point with its 'name', making the annotation vertical
for index, row in df_has_value.iterrows():
    plt.text(row['offset'], row['efficiency'], row['name'], 
             horizontalalignment='left', 
             size='medium', 
             color='black', 
             rotation=30)  # Rotate the text vertically
plt.ylim([0,1])
plt.xlabel('Offset (eV)')  # Adjust label as needed
plt.ylabel('Efficiency')
plt.title('Efficiency vs Offset')  # Adjust title as needed
plt.grid(True)  # Adds a grid
plt.savefig("measured-efficiency.png", dpi=600)
plt.show()


# Save csv

list_of_dicts = []
df_has_value = pd.DataFrame(columns=['name', 'IP', 'EA', 'offset', 'efficiency', 'doping'])

# Insert the modifications in your dictionary population loop
for material in yaml_data:
    dopant_ionization_rate = material['doping']['efficiency']['data']
    if dopant_ionization_rate and material['host'] not in exclude_hosts and material['dopant'] not in exclude_dopants:
        if list(dopant_ionization_rate.values())[0] is not None:
            tmp_dict = {
                'name': material['name'],
                'IP': material['IP']['value'],
                'EA': material['EA']['value'],
                'offset': material['IP']['value'] - material['EA']['value'],
                'efficiency': list(dopant_ionization_rate.values())[0],
                'doping': list(dopant_ionization_rate.keys())[0],
                'material_name': f"{material['host']}@{material['dopant']}"
            }
            list_of_dicts.append(tmp_dict)

df_has_value = pd.DataFrame(list_of_dicts)

# Create the scatter plot (as previously included)

# Save the DataFrame to a CSV
df_measured = df_has_value[df_has_value['efficiency'].notnull() & (df_has_value['efficiency'] > 0)]
df_measured[['material_name', 'efficiency']].to_csv('measured_efficiency.csv', index=False)
print("Data saved to 'measured_efficiency.csv'.")
