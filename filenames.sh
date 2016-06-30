#! /bin/sh

# create list of filenames and store in a temporary file
file="$1"
find "$file" -type f | grep -v "thumb\|.db" > tmp/filenames.txt

# parse file names to extract metadata columns, save as csv
python src/create_loadData.py

# reshape .csv file so that we have a column per channel
# and rename columns for CellProfiler
Rscript src/reshape.R

rm tmp/filenames.txt
rm tmp/py_load_long.csv