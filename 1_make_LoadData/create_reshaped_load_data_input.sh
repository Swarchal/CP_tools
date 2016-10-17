#!/bin/bash

# take directory location from stdin

# with directory being containing the load_data_inputs created from
# create_load_data_input.sh

# argument is the output location of the reshaped

# check user has passed at least one argument
if [ $# -eq 0 ]
then
    echo "ERROR: no arguments supplied"
    exit 1
fi


# read input from stdin and set to a variable
while read line
do
    var="${line}"
done < /dev/stdin


# check if we have a valid directory
if [ ! -d "$var" ]
then
    echo "ERROR: $var is not a valid directory"
    exit 1
else
    # for csv file in the directory
    for D in "$var"*".pre_load_data.csv"
    do
        # get the platename between last slash and dot
        platename_with_ext=${D%.*}
        platename=${platename_with_ext##*/}
        Rscript src/indv/reshape.R "${D}" "$1"/"$platename".csv
    done
fi

exit 0
