#! /bin/sh

# create list of filenames and store in a temporary file
echo " |█   | Creating file-list"
file="$1"
find "$file" -type f | grep -v "thumb\|.db" > tmp/filenames.txt

# parse file names to extract metadata columns, save as csv
echo " |██  | Extracting metadata"
python src/create_loadData.py

# reshape .csv file so that we have a column per channel
# and rename columns for CellProfiler
echo " |███ | Reshaping csv file"
Rscript src/reshape.R

echo " |████| Removing temporary files"
rm tmp/filenames.txt
rm tmp/py_load_long.csv