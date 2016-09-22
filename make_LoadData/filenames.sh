#! /bin/sh

# check that user has passed at least one argument

# if number of arguments is 0, then return error
if [ $# -eq 0 ]
    then
        echo "ERROR: No arguments supplied"
        exit 1
fi

# check optional metadata argument before creating file-list this is done before
# as creating the file-list is very slow so it's better to error as soon as
# possible if it's going to happen
if [ ! -z "$2" ] && [ ! -f "$2" ];
    then
        echo "ERROR: $2 does not exist"
        exit 1
fi

# create list of filenames and store in a temporary file
echo " |█    | Creating file-list"
# check the directory exists

# if directory does not exist
if [ ! -d "$1" ]
    then
        echo "ERROR: $1 is not a valid directory"
        exit 1
    else
	# find files that do not contain "thumb" or ".db"
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
    then
        echo "  - Metadata argument passed"
        python src/add_metadata.py "$2"
fi

echo " |█████| Removing temporary files"
rm tmp/filenames.txt
rm tmp/py_load_long.csv
exit 0
