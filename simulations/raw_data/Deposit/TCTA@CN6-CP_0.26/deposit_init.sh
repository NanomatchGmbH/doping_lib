#!/bin/bash


# Directly assign command-line arguments to variables without defaults
host=$1
dop=$2
nmol=$3
dx=$4
dy=$5
dz=$6

# Ensure all required arguments are provided
if [ -z "$host" ] || [ -z "$dop" ] || [ -z "$nmol" ] || [ -z "$dx" ] || [ -z "$dy" ] || [ -z "$dz" ]; then
    echo "Usage: $0 <host> <dop> <nmol> <dx> <dy> <dz>"
    exit 1
fi


WORKING_DIR=`pwd`
DATA_DIR=$WORKING_DIR

if [ -d $SCRATCH ]
then
    WORKING_DIR=$SCRATCH/`whoami`/`uuidgen`
    mkdir -p $WORKING_DIR
    cp -r $DATA_DIR/* $WORKING_DIR/
    cd $WORKING_DIR
fi

echo "Deposit running on node $(hostname) in directory $WORKING_DIR"
cd $WORKING_DIR

export DO_RESTART="False"
if [ "$DO_RESTART" == "True" ]
then
    if [ -f restartfile.zip ]
    then
        echo "Found Checkpoint, extracting for restart."
        unzip -q -o restartfile.zip
        rm restartfile.zip
    else
        echo "Restart was enabled, but no checkpoint file was found. Not starting simulation."
        exit 5
    fi
fi


Deposit molecule.0.pdb=molecule_0.pdb molecule.0.spf=dihedral_forcefield_0.spf molecule.0.conc=$host molecule.1.pdb=molecule_1.pdb molecule.1.spf=dihedral_forcefield_1.spf molecule.1.conc=$dop  simparams.Thi=4000.0 simparams.Tlo=300.0 simparams.sa.Tacc=5.0 simparams.sa.cycles=30 simparams.sa.steps=130000 simparams.Nmol=$nmol simparams.moves.dihedralmoves=True Box.Lx=$dx Box.Ly=$dy Box.Lz=$dz Box.pbc_cutoff=20.0 simparams.PBC=True machineparams.ncpu=${UC_PROCESSORS_PER_NODE} Box.grid_overhang=30

obabel structure.cml -O structure.mol2

if [ "True" == "True" ]
then
    $DEPTOOLS/add_periodic_copies.py 7.0
    mv periodic_output/structurePBC.cml .
    rm -f periodic_output/*.cml
    zip -r periodic_output_single_molecules.zip periodic_output
    rm -r periodic_output/
fi


zip restartfile.zip deposited_*.pdb.gz static_parameters.dpcf.gz static_parameters.dpcf_molinfo.dat.gz grid.vdw.gz grid.es.gz neighbourgrid.vdw.gz

rm deposited_*.pdb.gz deposited_*.cml static_parameters.dpcf.gz grid.vdw.gz grid.es.gz neighbourgrid.vdw.gz

if [ -d $SCRATCH ]
then
if [ -d $WORKING_DIR ]
then
    rsync -av $WORKING_DIR/* $DATA_DIR/ --exclude "*.stderr" --exclude "*.stdout" --exclude "stdout" --exclude "stderr"
    cd $DATA_DIR
    rm -r $WORKING_DIR
fi
fi

QuantumPatchAnalysis > DensityAnalysisInit.out
QuantumPatchAnalysis Analysis.Density.enabled=True Analysis.RDF.enabled=True #> DensityAnalysis.out

cat deposit_settings.yml >> output_dict.yml


