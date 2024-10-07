# DEPOSIT sml
forcefield_spec:
- - DepositLennardJonesGridStatic
  - depth: 3
    filename: grid.vdw.gz
    neighbourgrid_filename: neighbourgrid.vdw.gz
    static_pdb: dep3
    static_spf: merged.spf
    static_parameters_filename: static_parameters.dpcf.gz
    grid_min_x: -90
    grid_min_y: -90
    grid_min_z: -30
    grid_size_x: 180
    grid_size_y: 180
    grid_size_z: 540
    grid_spacing_x: 1
    grid_spacing_y: 1
    grid_spacing_z: 1
    scale: 1.0
- - DepositScreenElectrostatics
  - filename: grid.es.gz
    static_pdb: dep3
    static_spf: merged.spf
    static_parameters_filename: static_parameters.dpcf.gz
    grid_min_x: -90
    grid_min_y: -90
    grid_min_z: -30
    grid_size_x: 180
    grid_size_y: 180
    grid_size_z: 540
    grid_spacing_x: 1
    grid_spacing_y: 1
    grid_spacing_z: 1
    scale: 1.0
    ewald: False
    box_size: 10000.000000
- - ZDrivingPotential
  - scale: 1.0
    steepness: 1.000000
    z0: 0.0
    cutoff: 0.0
    subunits: "-1"
- - DepositCOMPlaneDistPot
  - cutoff_energy: 100.0
    k: 120.000
    scale: 1.0
    subunits: '-1'
    z0: 0.0
    zmax_cutoff: 3.0
- - DepositInternalOpenMM
  - depth: 4
    subunits: "-2"
    scale: 1.0
    coulomb: True
    sixten: True
- - SIMONASplineDihedralPotentialV2
  - scale: 1.0
moves:
  analysis_moves:
  - - print_energy
    - begin_step: 0
      last_step: 0
      step_mod: 5000
  - - trajectory
    - begin_step: 0
      fname: trajectory.pdb.gz
      last_step: 0
      only_new: 0
      step_mod: 10000000
  initial: []
  list:
  - - deposit_rigid_active_trans_pbc
    - delta: 1.000000
      subunits: "-1"
      Lx: 60.000000
      Ly: 60.000000
      alpha: 90.000000
  - - deposit_active_rigid_rot
    - delta: 3.141593
      subunits: "-1"
  - - deposit_active_dihedrals
    - delta_phi_max: 0.523599
      mode: 'RelativeRandom'
nsteps: 30
peptide_spec: false
preprocessor:
  SPF_VERSION: 2
  algorithm:
    name: deposit
    params:
      Nmol: 3500
      out_checkpoint_freq: 500
      static_parameters_filename: static_parameters.dpcf.gz
      grid_min_x: -60.000000
      grid_min_y: -60.000000
      grid_size_x: 120.000000
      grid_size_y: 120.000000
      parallel_runs: 76
      alpha: 90.000000
      dz_cutoff: 10.000000
      z_shift: 20.000000
      pbc: True
      pbc_cutoff: 20.000000
      kB: 0.0019858775
      mps: 1
      quantum_deposit: False
      dynamic_update: False
      dynamic_layerwidth: 15.000000
      dynamic_extralayer: -1.000000
      dynamic_stepmod: 300
      crystal: False
      postrelaxation_steps: 0
      concentrations:
      - 0.74
      - 0.26
      sa_list:
      - energymodel_nr: 0
        nsteps: 130000
        tstart: 4000.000000
        tend: 300.000000
        tscaling: geometric
  atom_params: merged.spf  
  name: nano
  simonaparser_use_bonds: false
  simonapdbparser_auto_rename: false
  simonapdbparser_connects: false
  simonapdbparser_occ_as_charge: false
  treat_unknown: fatal
  use_simona_pdb_parser: true
print_level: 1
seed: random
sourceFormat: 5
tstart: 5.000000
tend: 5.000000
verboseDihedral: false
warn_level: 5
xml_indent: true
