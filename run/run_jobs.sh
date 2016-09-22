#!/bin/bash

# run all submission scripts
# argv is the directory containing all SGE submission scripts create by
# batch_insert

if [ $# -eq 0 ]; then
    echo "ERROR: No arguments supplied"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "ERROR: $1 is not a valid directory"
    exit 1
fi

# create file listing all submission scripts
ls "$1" > .jobs_to_run.txt

# run all submission scripts
while read job; do
    qsub $job
done < jobs_to_run.txt

rm .jobs_to_run.txt

exit 0