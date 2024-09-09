import os
import yaml
import pandas as pd
from yaml.constructor import ConstructorError

class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
    def ignore_unknown(self, node):
        return None

SafeLoaderIgnoreUnknown.add_constructor(None, SafeLoaderIgnoreUnknown.ignore_unknown)

def extract_data_from_folder(base_path):
    data = []
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path) and 'lightforge_data' in os.listdir(folder_path):
            file_path = os.path.join(folder_path, 'lightforge_data', 'runtime_data', 'x_y_summary.yml')
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    try:
                        contents = yaml.load(file, Loader=SafeLoaderIgnoreUnknown)
                        n_dop = contents['ion_doping']['Temperature']['n_dop'][0]
                        n_ion_p_dop = contents['ion_doping']['Temperature']['n_ion_p_dop'][0]
                        ionization = n_ion_p_dop / n_dop
                        fraction = folder.split('@')[-1].split('-')[-1]
                        data.append({'material': folder, 'fraction': fraction, 'ionization': ionization})
                    except ConstructorError:
                        print(f"Error processing file {file_path}: contains unconstructable Python objects.")
                    except KeyError as e:
                        print(f"Missing expected data in {file_path}: {e}")
    return data

base_directory = os.getcwd()

results = extract_data_from_folder(base_directory)

df = pd.DataFrame(results)
df.to_csv('ionization_data.csv', index=False)

