# run in the folder with simulation folders containing doping ionization simulations
import os
import yaml
import pandas as pd
import ast
from yaml.constructor import ConstructorError

output_filename = 'ionization_ip_ea.csv' # <-- material, fraction, ionization, ip, ea


class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
    def ignore_unknown(self, node):
        return None

SafeLoaderIgnoreUnknown.add_constructor(None, SafeLoaderIgnoreUnknown.ignore_unknown)

def extract_fraction_from_folder(folder_name):
    # Extract fraction from folder name, e.g., 'BPAPF@CN6-CP_0.26' -> '0.26'
    try:
        fraction_part = folder_name.split('_')[-1]
        # Remove any non-numeric characters
        fraction = ''.join(c for c in fraction_part if c.isdigit() or c == '.')
        return fraction
    except IndexError:
        return None

def extract_ionization(folder_path):
    file_path = os.path.join(folder_path, 'lightforge_data', 'runtime_data', 'x_y_summary.yml')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                contents = yaml.load(file, Loader=SafeLoaderIgnoreUnknown)
                n_dop = contents['ion_doping']['Temperature']['n_dop'][0]
                n_ion_p_dop = contents['ion_doping']['Temperature']['n_ion_p_dop'][0]
                ionization = n_ion_p_dop / n_dop
                return ionization
            except ConstructorError:
                print(f"Error processing file {file_path}: contains unconstructable Python objects.")
            except KeyError as e:
                print(f"Missing expected data in {file_path}: {e}")
    return None

def extract_ip_ea(folder_path):
    settings_path = os.path.join(folder_path, 'settings.yml')
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as file:
            data = yaml.safe_load(file)
        ip_host = None
        ea_dopant = None
        for material in data.get('materials', []):
            if 'energies' in material['molecule_parameters']:
                energies_str = material['molecule_parameters']['energies']
                try:
                    energies = ast.literal_eval(energies_str)
                except (SyntaxError, ValueError):
                    print(f"Error parsing energies in {settings_path}")
                    continue
                if not material['molecule_parameters'].get('is_dopant', False):
                    ip_host = energies[0][0]
                elif material['molecule_parameters'].get('is_dopant', False):
                    ea_dopant = energies[0][1]
        return ip_host, ea_dopant
    return None, None

def main():
    base_directory = os.getcwd()
    data = []
    for folder in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder)
        if os.path.isdir(folder_path):
            data_entry = {}
            data_entry['material'] = folder
            data_entry['fraction'] = extract_fraction_from_folder(folder)
            ionization = extract_ionization(folder_path)
            if ionization is not None:
                data_entry['ionization'] = ionization
            ip, ea = extract_ip_ea(folder_path)
            if ip is not None:
                data_entry['IP'] = ip
            if ea is not None:
                data_entry['EA'] = ea
            data.append(data_entry)
    df = pd.DataFrame(data)
    df.to_csv(f'{output_filename}', index=False)
    print(f"Data extraction complete. Saved to {output_filename}.")

if __name__ == "__main__":
    main()

