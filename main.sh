#!/bin/bash

if [ ! $# -eq 3 ]
then
    echo "ERROR: need to supply exactly three arguments"
    echo "arg 1: plate location"
    echo "arg 2: output location"
    echo "arg 3: cellprofiler pipeline name"
    exit 1
fi


PLATE_LOCATION=$1
OUTPUT_LOCATION=$2
PIPELINE=$3


# clear tmp directory
rm .1_make_LoadData/tmp/*


# create image lists
1_make_LoadData/create_image_list.sh "$PLATE_LOCATION" | \
    1_make_LoadData/load_data.sh "$OUTPUT_LOCATION" | \
    1_make_LoadData/reshape.sh "$OUTPUT_LOCATION"


# loop through loadData files
batch_listify() {
    2_batch_LoadData/batch_list.py --file_list "$2"/"$1" \
                                   --pipeline "$3" \
        > ./tmp/batch_lists/"$1".batch
}

mkdir ./tmp/batch_lists/
for file in "$OUTPUT_LOCATION"
do batch_listify "$file" "$OUTPUT_LOCATION" "$PIPELINE" &
done

wait ${!}


# batch_insert
BATCH_LOCATION="$./tmp/batch_lists/"

batch_insert() {
    3_batch_insert/batch_script.py --batch_file "$1" -o "$2"
}

for f in "$BATCH_LOCATION"
do
    batch_insert "$f" "$OUTPUT_LOCATION" &
done

wait ${!}

exit 0
