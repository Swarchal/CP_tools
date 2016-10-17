#!/bin/bash

# takes a directory path of file-lists:
#   - parses metadata
#   - reshapes

# arguments
# ----------
# first argument: directory name containing file-lists
# second argument (optional) output location

# should only read in files with .filelist extension
# as we may have other files in the same directory

# check user has passed at least one argument
if [ $# -eq 0 ]
then
    echo "ERROR: no arguments supplied"
    exit 1
fi



create_load_data() {
    # get platename between last slash and dot
    platename_with_file=${D%.*}
    platename=${platename_with_file##*/}
    # extract metadata from image headings
    python src/indv/create_loadData.py "${D}" "$2"/"$platename".load_data.csv
}


# capture directory from stdin
while read line
do
    var="${line}"
done < /dev/stdin


if [ ! -d $var ]
then
    echo "ERROR $var is not a valid directory"
    exit 1
else
    # loop through image-list files and call create_loadData on each
    for D in "$var"*.filelist
    do
        create_load_data "${D}" "$1" &
    done
fi

echo "$1"

# wait 'till last background process has finished before exiting
wait ${!}

exit 0
