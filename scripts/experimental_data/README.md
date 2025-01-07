# Scripts to visualize [experimental_data](https://github.com/NanomatchGmbH/doping_lib/tree/main/experimental_data)

The script have in common that the raw experimental data, such as [doped_materials.yaml](https://github.com/NanomatchGmbH/doping_lib/blob/main/experimental_data/doped_materials.yaml) will be summarized and visualized. Analysis results are saved in the folder [summary](https://github.com/NanomatchGmbH/doping_lib/tree/main/experimental_data/summary)

## Script description
- measured_efficiency.py : output the information about about the materials where doping efficiency were experimentally measured. Generated data: `measured_efficiency.csv`, Generated visualization: `measured_efficiency.png`. Note: - you can ignore some dopants and hosts.
- work_or_not.py: plot materials classification in a binary fasion, i.e. if the doping works or does not work.
- basic analysis.py: output number of host and dopant materials and other basic information.
