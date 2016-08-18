from __future__ import print_function
import os
import pandas as pd
import numpy as np
import colfuncs
from sqlalchemy import create_engine

def _check_agg_func(agg_func):
    """check if agg_func is a valid function"""
    valid_agg_funcs = ["median", "mean"]
    if agg_func not in valid_agg_funcs:
        ValueError("Invalid agg_func, options are: 'median', 'mean'")

class ResultsDirectory:

    """
    Directory containing the .csv from a CellProfiler run
    ------------------------------------------------------
    - create_db(): creates an sqlite database in the results directory
        directory - string, top level directory containing cellprofiler output
    - to_db(): loads the csv files in the directory and writes them as
               tables to the sqlite database created by create_db()
        select - string, name of .csv ouput file, and subsequent table in db
        header - int or list, line numbers (0-indexed) of column headers, if a
                 a single header, then use 0 rather than [0].
    """

    def __init__(self, directory):
        """
        Get full filepaths of all files in a directory, including sub-directories
        """
        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
            self.file_paths = file_paths


    # create sqlite database
    def create_db(self, location, db_name="results"):
        self.db_handle = "sqlite:///%s/%s.sqlite" % (location, db_name)
        self.engine = create_engine(self.db_handle)


    # write csv files to database
    def to_db(self, select="DATA", header=0):
        """
        select - string, the name of the .csv file, this will also be the
                 database table
        header - int or list, the number of header rows.
                N.B. if not multi-indexed then use 0 rather than [0].
        """
        # filter files
        file_paths = [f for f in self.file_paths if f.endswith(select+".csv")]

        for x in file_paths:
            if header == 0:
                # dont need to collapse headers
                print("importing :", x)
                tmp_file = pd.read_csv(x, header=header, chunksize=10000,
                        iterator=True)
                all_file = pd.concat(tmp_file)
                all_file.to_sql(select, con=self.engine, flavor="sqlite",
                        index=False, if_exists="append")
            else:
                # have to collapse columns, means reading into pandas
                print("importing :", x)
                tmp_file = pd.read_csv(x, header=header, chunksize=10000,
                    iterator=True)
                all_file = pd.concat(tmp_file)
                # collapse column names if multi-indexed
                if isinstance(all_file.columns, pd.core.index.MultiIndex):
                    all_file.columns = colfuncs.collapse_cols(all_file)
                else:
                    TypeError("Multiple headers selected, yet dataframe is not multi-indexed")
                all_file.to_sql(select, con=self.engine,
                    flavor="sqlite", index=False, if_exists="append")


    def to_db_agg(self, select="DATA", header=0, by="ImageNumber",
                  agg_func="median"):
        """
        select - string, the name of the .csv file, this will also be the
                 prefix of the database table name.
        header - int or list, the number of header rows.
                 N.B if not multi-indxed, then use 0 rather than [0].
        by - string, the column by which to group the data by.
        """

        # check agg_func is a valid function
        _check_agg_func(agg_func)

        # filter files
        file_paths = [f for f in self.file_paths if f.endswith(select+".csv")]

        for x in file_paths:
            if header == 0:
                print("importing :", x)
                tmp_file = pd.read_csv(x, header=header)
                tmp_grouped = tmp_file.groupby(by, as_index=False)
                if agg_func == "median":
                    tmp_agg = tmp_grouped.aggregate(np.median)
                elif agg_func == "mean":
                    tmp_agg = tmp_grouped.aggregate(np.mean)
                tmp_agg.to_sql(select+"_agg", con=self.engine, flavor="sqlite",
                               index=False, if_exists="append")
            else:
                print("importing :", x)
                tmp_file = pd.read_csv(x, header=header)
                # collapse multi-indexed columns
                if isinstance(tmp_file.columns, pd.core.index.MultiIndex):
                    tmp_file.columns = colfuncs.collapse_cols(tmp_file)
                else:
                    TypeError("Multiple headers selected, yet dataframe is not multi-indexed")
                tmp_grouped = tmp_file.groupby("Image_"+by, as_index=False)
                if agg_func == "median":
                    tmp_agg = tmp_grouped.aggregate(np.median)
                elif agg_func == "mean":
                    tmp_agg = tmp_grouped.aggregate(np.mean)
                tmp_agg.to_sql(select+"_agg", con=self.engine, flavor="sqlite",
                               index=False, if_exists="append")



if __name__ == '__main__':
    x = ResultsDirectory("/mnt/datastore/scott/2016-07-13_SGC/raw_data")
    x.create_db("/home/scott/2016-07-13_SGC/")
    x.to_db_agg(select="DATA", header=[0,1])
    x.to_db(select="DATA", header=[0,1])
    x.to_db(select="IMAGE", header=[0,1])
