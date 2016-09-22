#! /usr/bin/env python

import pandas as pd
import parse_path as pp

"""
Convert file paths into a .csv file ready for loadData module in CellProfiler
"""

text = "tmp/filenames.txt"


colnames = ["URL", "path", "Metadata_platename", "Metadata_well",
            "Metadata_site", "Metadata_channel", "Metadata_platenum"]

# sanity check filenames
with open(text) as f:
    filenames = pp.get_filename(text)
    pp.check_filename(filenames)

df = pd.DataFrame(
                  zip(filenames,
                      pp.get_path(text),
                      pp.get_platename(text),
                      pp.get_metadata_well(text),
                      pp.get_metadata_site(text),
                      pp.get_metadata_channel(text),
                      pp.get_platenum(text))
)

df.columns = colnames

"""
Need to re-order so that each image has it's own line, with a column
per channel number.
"""

# write long format to csv to reshape in R
df.to_csv("tmp/py_load_long.csv", index_label=False)
