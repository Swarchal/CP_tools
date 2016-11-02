#!/bin/bash

###############################################################################
# automatically generate cellprofiler submission scripts to be run on SGE
# from a ImageExpress file directory
#
# Arguments:
# -----------
#   -f : directory containing plates in the ImageXpress file directory that
#        can be accessed by the cluster.
#   -s : path to user's scratch space
#   -p : path to cellprofiler pipeline beginning with a LoadData module
###############################################################################

###############################################################################
# PARSE ARGUMENTS
###############################################################################

# check number of arguments supplied
if [ $# -eq 0 ]
then
    echo "ERROR: no arguments supplied"
    exit 1
fi

# getopts to parse arguments
OPTIND=1
while getopts f:s:p: opts
do
    case ${opts} in
        f) IMG_LOC=${OPTARG} ;;
        s) SCRATCH=${OPTARG} ;;
        p) PIPLINE_LOC=${OPTARG} ;;
    esac
done

# make submission scripts directory if it doesn't exist
if [ ! -d submission_scripts ]
then
    mkdir submission_scripts
fi

if [ ! -d batch_commands ]
then
    mkdir batch_commands
fi

###############################################################################
# 1 CREATE FILE LISTS
###############################################################################

cd 1_make_LoadData

# store file-lists contained in tmp
ls tmp > ../.file_lists.txt

###############################################################################
# 2 CREATE LOADDATA FILES
###############################################################################

# get path location of tmp file
cd tmp
tmp_loc=${pwd}

cd ../../2_batch_LoadData

while read f
do
    ./batch_list.py -f "$tmp_loc"/"$f" -p "$PIPELINE_LOC" > ../batch_commands/"$f"
done < ../.file-list.txt


###############################################################################
# 3 INSERT CELLPROFILER COMMANDS INTO SGE SUBMISSION SCRIPTS
###############################################################################


cd ../batch_commands
# get path location of batch_files
batch_loc=${pwd}
# get list of batch command files and store as a text file for loop
ls > ../.batch_list.txt

# move to directory containing batch_insert module
cd ../3_batch_insert

# loop through list of batch_lists and insert into SGE submission script
# (templace_job.sh)
while read f
do
    ./batch_script.py -f "$batch_loc"/"$f" \
        -t template_job.sh
        -o ../submission_scripts/
done < ../.batch_list.txt


exit 0