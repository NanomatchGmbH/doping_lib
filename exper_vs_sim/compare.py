import pandas as pd
import os

def main():
    # Define paths to the files
    efficiency_path = '../measured_efficiency.csv'
    simulation_path = '../results/0/ionization_ip_ea.csv'

    # Load the data
    df_efficiency = pd.read_csv(efficiency_path)
    df_simulation = pd.read_csv(simulation_path)

    # Normalize the 'material' columns by splitting on '_' and taking the first part
    df_efficiency['material_normalized'] = df_efficiency['material_name'].apply(lambda x: x.split('_')[0])
    df_simulation['material_normalized'] = df_simulation['material'].apply(lambda x: x.split('_')[0])

    # Rename columns for clarity
    df_efficiency.rename(columns={'efficiency': 'experiment'}, inplace=True)
    df_simulation.rename(columns={'ionization': 'simulation'}, inplace=True)

    # Merge the DataFrames on the normalized material field
    df_merged = pd.merge(df_efficiency[['material_normalized', 'experiment']],
                         df_simulation[['material_normalized', 'simulation', 'IP', 'EA']],
                         on='material_normalized',
                         how='outer')

    # Save the merged DataFrame to a new CSV file
    output_path = 'merged_ionization_data.csv'
    df_merged.to_csv(output_path, index=False)
    print("Merged data saved to", output_path)

if __name__ == "__main__":
    main()

