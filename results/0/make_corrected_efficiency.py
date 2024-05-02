import pandas as pd

REFERENCE_MATERIAL = "BFDPB@CN6-CP_0.26"

TO_BE_CORRECTED = [
    "BFDPB@CN6-CP",
    "NPB@CN6-CP",
    "BPAPF@CN6-CP",
    "TCTA@CN6-CP"
]

simulation_df = pd.read_csv("ionization_data.csv")

reference_value = simulation_df[simulation_df["material"] == REFERENCE_MATERIAL]["ionization"].iloc[0]

print(f"{reference_value=}")

measured_efficiency = pd.read_csv("../../measured_efficiency.csv")

print(f"{measured_efficiency=}")

# todo add field efficiency_corrected
measured_efficiency['efficiency_updated'] = measured_efficiency['efficiency']


for material in TO_BE_CORRECTED:
    if measured_efficiency["material_name"].isin([material]).any():
        print(material)
        # measured_efficiency[material]["efficiency_updated"] = reference_value * measured_efficiency[material]["efficiency"]
        measured_efficiency.loc[measured_efficiency["material_name"] == material, "efficiency_updated"] = reference_value * measured_efficiency.loc[measured_efficiency["material_name"] == material, "efficiency"]

print(f"{measured_efficiency=}")

measured_efficiency.to_csv("corrected_measured_efficiency.csv", index=False)
