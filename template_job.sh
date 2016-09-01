#!/bin/sh
#$ -l h_vmem=12G
#$ -l h_rt=12:00:00
#$ -j y
#$ -o /exports/eddie/scratch/$(whoami)/cp_$(date +%F).log

. /etc/profile.d/modules.sh
module load igmm/apps/hdf5/1.8.16
module load igmm/apps/python/2.7.10
module load igmm/apps/jdk/1.8.0_66
module load igmm/libs/libpng/1.8.18
source /home/$(whoami)/virtualenv-1.10/myVE/bin/activate
source /home/$(whoami)/.bash_profile

# directory containing images list and pipeline
# or could use absolute paths in the pipeline commands

# placeholder string to be substituted with cellprofiler command
PLACEHOLDER
