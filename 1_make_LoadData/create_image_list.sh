#!/bin/bash

# creates file-list on a plate-by-plate basis
# first argument: directory containing plate subdirectories
# second argument (optional) : output location for filename files

# outputs location of file-list

# check that user has passed at least one argument
# if number of arguments is 0, then return error
if [ $# -eq 0 ]
then
    echo "ERROR: No arguments supplied"
    exit 1
fi


# if no second argument has been passed, then save to tmp
if [ ! -z "$2"]
then
    output=$2
else
    output="$PWD/tmp/"
fi


create_load_data() {
    # get final platename from the filepath to prefix
    # the $_filenames.txt
    platename=$(echo "${D}" | sed "s/.*\///")
    find "${D}" -type f | grep -v "thumb\|.db" > \
    "$output"/"$platename".filelist
}


# check the directory exists
if [ ! -d "$1" ]
# if directory does not exist
then
    echo " ERROR: $1 is not a valid directory"
    exit 1
else
    # for every subdirectory in directory parent directory
    for D in "$1"*
    do
        create_load_data "${D}" "$output" &
    done
fi

wait ${!}

# return directory location of image_lists
# so we can pipe to next function that takes this as an argument
echo $output

exit 0
