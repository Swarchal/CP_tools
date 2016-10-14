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


# check the directory exists
if [ ! -d "$1" ]
# if directory does not exist
then
    echo " ERROR: $1 is not a valid directory"
    exit 1
else
    # for every subdirectory in directory parent directory
    # find files that do not contain "thumb" or ".db"
    for D in "$1"*;
    do
        if [ -d "${D}" ]
        then
            # get final platename from the filepath to prefix
            # the $_filenames.txt
            platename=$(echo "${D}" | sed "s/.*\///")
            if [ ! -z "$2" ]
            then
                # if second argument has been passed
                # save to the argument location
                find "${D}" -type f | grep -v "thumb\|.db" > \
                "$2"/"$platename".filelist
            else
                # save to ./tmp/
                find "${D}" -type f | grep -v "thumb\|.db" > \
                tmp/"$platename".filelist
            fi
        fi
    done
fi

# return directory location of image_lists
# so we can pipe to next function that takes this as an argument
if [ ! -z "$2" ]
then
    echo "$2"
else
    echo "$PWD/tmp"
fi

exit 0
