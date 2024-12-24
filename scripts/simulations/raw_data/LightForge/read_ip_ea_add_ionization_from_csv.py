import os
import yaml
import pandas as pd
import ast


existing_csv_path = 'ionization_data.csv'
new_csv_path = 'new_ionization_data.csv'


def extract_ip_ea_from_yaml(filepath):
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    ip_host = None
    ea_dopant = None
    for material in data.get('materials', []):
        if 'energies' in material['molecule_parameters']:
            energies_str = material['molecule_parameters']['energies']
            energies = ast.literal_eval(energies_str)
            if not material['molecule_parameters'].get('is_dopant', False):
                ip_host = energies[0][0]
            elif material['molecule_parameters'].get('is_dopant', False):
                ea_dopant = energies[0][1]
    return ip_host, ea_dopant

def main():
    # Create a DataFrame to store the extracted data
    new_data = pd.DataFrame(columns=['material', 'IP', 'EA'])
    
    # Navigate through all folders in the current directory
    for folder in os.listdir():
        if os.path.isdir(folder):
            settings_path = os.path.join(folder, 'settings.yml')
            if os.path.exists(settings_path):
                ip, ea = extract_ip_ea_from_yaml(settings_path)
                # Append new row to DataFrame using pd.concat
                new_row = pd.DataFrame({'material': [folder], 'IP': [ip], 'EA': [ea]})
                new_data = pd.concat([new_data, new_row], ignore_index=True)
    
    # Save the new data to a CSV file
    new_data.to_csv(new_csv_path, index=False)
    
    # Check if there is an existing 'ionization_data.csv' and merge if it exists
    existing_csv_path = 'ionization_data.csv'
    if os.path.exists(existing_csv_path):
        existing_data = pd.read_csv(existing_csv_path)
        combined_data = pd.merge(existing_data, new_data, on='material', how='outer')
        combined_data.to_csv(existing_csv_path, index=False)
    else:
        # If 'ionization_data.csv' does not exist, rename the new CSV
        os.rename(new_csv_path, existing_csv_path)

    print("Operation completed. Data has been processed and saved.")

if __name__ == "__main__":
    main()

