"""
- name: "Spiro-TAD:F6TCNNQ"
  dopant: F6TCNNQ
  host: Spiro-TAD
  concentration: {units: "mol%", data: [0.0, 0.5, 1.0, 2.0, 4.5, 10.0]}
  doping:
    works: true
    efficiency: {method: null, data: null}
  doi: "10.1002/adfm.201703780"
  full_text: "https://oar.princeton.edu/jspui/bitstream/88435/pr1hm9f/1/Zhang%20%20Kahn%20Adv.%20Funct.%20Mat.%202017.pdf"
  EA: {value: 5.6, method: IPES}
  IP: {value: 5.46, method: UPS}
  additional_info: null
"""
import pathlib
from enum import Enum
import yaml

LIB = 'lib.yaml'
FICTIONAL_P3HT_LIB = 'lib_fictional_p3ht.yaml'

class Mol2Folders(Enum):
    DOPANT_FOLDER = pathlib.Path('mol2/dopant')
    HOST_FOLDER = pathlib.Path('mol2/host')
    FICTOINAL_P3HT_FOLDER = pathlib.Path('mol2/fictional_p3ht')


def get_yaml(yaml_file):
    with open(yaml_file) as fid:
        return yaml.load(fid, Loader=yaml.CLoader)


doping_lib = get_yaml(LIB)
fictional_p3ht_lib = get_yaml(FICTIONAL_P3HT_LIB)

class MolType(Enum):
    DOPANT = 'dopant'
    HOST = 'host'


def get_all_mol_of_type(dop_lib: dict, mtype: MolType) -> set:
    all_mol_given_type = set()
    for mol in dop_lib:
        all_mol_given_type.add(mol[mtype.value])
    return all_mol_given_type


def check_folder_has_mols(mol2_folder: pathlib.Path, mol_names: set):
    missing_mols = set()
    for mol_name in mol_names:
        xyz_name = mol_name + '.mol2'
        path_to_xyz = mol2_folder / xyz_name
        if not path_to_xyz.exists():
            missing_mols.add(path_to_xyz.name)
    return missing_mols


# 1
print("1)")
total_num_doped_materials = 0
for material in doping_lib:
    total_num_doped_materials += 1
    print(f"{material['name']=}")
print(f"{total_num_doped_materials=}")

# 2
print("1)")
print(f"{get_all_mol_of_type(doping_lib, MolType.HOST)=}")
print(f"{get_all_mol_of_type(doping_lib, MolType.DOPANT)=}")
print(f"{get_all_mol_of_type(fictional_p3ht_lib, MolType.HOST)=}")

# 3.1. host
print("3.1. host")
missing_host_molecules = check_folder_has_mols(
    mol2_folder=Mol2Folders.HOST_FOLDER.value, mol_names=get_all_mol_of_type(doping_lib, mtype=MolType.HOST)
)
print(f"{missing_host_molecules=}")

# 3.2. dopant
print("3.2. dopant")
missing_dopant_molecules = check_folder_has_mols(
    mol2_folder=Mol2Folders.DOPANT_FOLDER.value, mol_names=get_all_mol_of_type(doping_lib, mtype=MolType.DOPANT)
)
print(f"{missing_dopant_molecules=}")

# 3.3. fictional P3HT
print("3.2. fictional p3ht host (in fact, nT)")
missing_dopant_molecules = check_folder_has_mols(
    mol2_folder=Mol2Folders.FICTOINAL_P3HT_FOLDER.value, mol_names=get_all_mol_of_type(fictional_p3ht_lib, mtype=MolType.HOST)
)
print(f"{missing_dopant_molecules=}")
