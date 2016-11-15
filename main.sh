#!/bin/bash
#-------------------------------------------------------------------------------
# Abandon all hope ye who enter here...
#
# This is a convoluted mess of bash/sed/grep, python and R, all using a mix of
# command line args and stdin.
#
# I have no idea of how it all works and it's probably developed some sort of
# sentience, so be absolutely sure before changing anything as there are zero
# tests.
#------------------------------------------------------------------------------

###############################################################################
# automatically generate cellprofiler submission scripts to be run on SGE
# from a ImageExpress file directory
#
# Arguments:
# -----------
#   -f : directory containing plates in the ImageXpress file directory that
#        can be accessed by the cluster. NOTE need an absolute file path
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
if [ ! -d file_lists ]
then
    mkdir file_lists
    if [ ! -d file_lists ]
    then
        echo "ERROR: failed to create file_lists directory"
        exit 1
    fi
fi


if [ ! -d batch_commands ]
then
    mkdir batch_commands
    if [ ! -d batch_commands ]
    then
        echo "ERROR: failed to create batch_commands directory"
        exit 1
    fi
fi


if [ ! -d submission_scripts ]
then
    mkdir submission_scripts
    if [ ! -d submission_scripts ]
    then
        echo "ERROR failed to create submission scripts directory"
	exit 1
    fi
fi


###############################################################################
# 1 CREATE FILE LISTS
###############################################################################

# get full path of file_lists directory
# NOTE this means that we need an absolute file path
cd file_lists
file_lists_loc="$(pwd)"

cd ../1_make_LoadData

./create_load_data.sh "$IMG_LOC" "$file_lists_loc"

# create list of file_lists
cd ../file_lists
ls > ../.file-list.txt


###############################################################################
# 2 CREATE LOADDATA FILES
###############################################################################

cd ../2_batch_LoadData

while read f
do
    ./batch_list.py --file_list "$file_lists_loc"/"$f" \
        --pipeline "$PIPELINE_LOC" \
        --path_prefix "$SCRATCH" > ../batch_commands/"$f"
done < ../.file-list.txt


###############################################################################
# 3 INSERT CELLPROFILER COMMANDS INTO SGE SUBMISSION SCRIPTS
###############################################################################


cd ../batch_commands
# get path location of batch_files
batch_loc=$(pwd)
# get list of batch command files and store as a text file for loop
ls > ../.batch_list.txt

# move to directory containing batch_insert module
cd ../3_batch_insert

# loop through list of batch_lists and insert into SGE submission script
# (templace_job.sh)
while read f
do
    ./batch_script.py --batch_file "$batch_loc"/"$f" \
        --template template_job.sh \
        --output_location ../submission_scripts/
done < ../.batch_list.txt


exit 0
