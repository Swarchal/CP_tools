#!/bin/sh
#$ -l h_vmem=12G
#$ -l h_rt=12:00:00
#$ -j y
#$ -o /exports/eddie/scratch/s1027820/cp.log

. /etc/profile.d/modules.sh
module load igmm/apps/hdf5/1.8.16
module load igmm/apps/python/2.7.10
module load igmm/apps/jdk/1.8.0_66
module load igmm/libs/libpng/1.8.18

source /exports/igmm/eddie/Drug-Discovery/virtualenv-1.10/myVE/bin/activate
source ~/.bash_profile

# placeholder string to be substituted with cellprofiler command
PLACEHOLDER
