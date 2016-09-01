#! /bin/sh

# check that user has passed at least one argument
if [ $# -eq 0 ]
    then
        echo "ERROR: No arguments supplied"
        exit 1
fi

# create list of filenames and store in a temporary file
echo " |█    | Creating file-list"
# check the directory exists
if [ ! -d "$1" ]
    then
        echo "ERROR: $1 is not a valid directory"
        exit 1
    else
        file="$1"
        find "$file" -type f | grep -v "thumb\|.db" > tmp/filenames.txt
fi

# parse file names to extract metadata columns, save as csv
echo " |██   | Extracting metadata from filenames"
python src/create_loadData.py

# reshape .csv file so that we have a column per channel
# and rename columns for CellProfiler
echo " |███  | Reshaping csv file"
Rscript src/reshape.R

echo " |████ | Merging any external metadata"
if [ ! -z "$2" ];
    # if there is a second argument
    then
        if [ ! -f "$2" ]
            # check the external metadata file exists
            then
                # if not, then clean-up and exit
                echo "ERROR: $2 is not a valid file"
                rm tmp/filenames.txt
                exit 1
            else
                # if file is good, then pass to python script
                echo "  - Metadata argument passed"
                python src/add_metadata.py "$2"
        fi
fi

echo " |█████| Removing temporary files"
rm tmp/filenames.txt
rm tmp/py_load_long.csv
exit 0
