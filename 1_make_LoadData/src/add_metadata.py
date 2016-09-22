from sys import argv
import pandas as pd

"""
Merge external metadata csv file with file-list, by well and plate label
If no plate_label is supplied, then just merge by well

For the external metadata, columns need to be labelled
 - Metadata_well
 - Metadata_platename
All other columns labelled Metadata_
well be added to the file-list
"""

# note argv[1] in this case, as we are only passing the second argument to this
# python script
metadata_file = argv[1]
# load the external metadata
metadata = pd.read_csv(str(metadata_file))
# load the reshaped file list
file_list = pd.read_csv("load_data_input.csv")

metadata_cols = [col for col in metadata.columns if col.startswith("Metadata_")]

if len(metadata_cols) < len(metadata.columns):
    raise Warning("some columns are not prefixed with Metadata_" +
                  " and have not been merged")

if "Metadata_platename" in metadata_cols:
    # if we have metadata plate in the metadata file
    # then merge using well and plate
    df_merged = file_list.merge(metadata, on=["Metadata_well",
                                              "Metadata_platename"])
else:
    # otherwise, just merge by well
    df_merged = file_list.merge(metadata, on="Metadata_well")

df_merged.to_csv("load_data_input.csv", index_label=False)
