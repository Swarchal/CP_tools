import os
import pandas as pd
import sys

if len(sys.argv) < 2:
    raise AttributeError("Expecting argv argument for directory containing .csv files")

my_path = sys.argv[1]

def get_filepaths(directory):
    """Get full filepaths of all files in a directory, including sub-directories"""
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths

# Run the above function and store its results in a variable.
files = get_filepaths(my_path)

# N.B header=[0,1] is assuming we have multi-indexed columns from cellprofiler
df = pd.concat((pd.read_csv(f, header=[0,1]) for f in files if f.endswith(".csv")))

# if given an ouput location, else save in cwd
if len(sys.argv) == 3:
    outplace = sys.argv[2]
else:
    outplace = os.getcwd()

out_path = os.path.join(outplace, "merged_output.csv")
df.to_csv(out_path)
