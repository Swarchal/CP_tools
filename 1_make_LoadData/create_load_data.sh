#!/bin/bash

if [ ! $# -eq 2 ]
then
    echo "ERROR: need to supply exactly two arguments"
    exit 1
fi

# clear tmp directory
rm ./tmp/*

./create_image_list.sh "$1" | \
./load_data.sh "$2" | \
./reshape.sh "$2"

exit 0
