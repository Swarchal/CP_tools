from __future__ import print_function
import os
import pandas as pd
import numpy as np
import colfuncs
from sqlalchemy import create_engine


class ResultsDirectory(object):

    """
    Directory containing the .csv from a CellProfiler run

    Methods
    -------
    create_db :
        creates an sqlite database in the results directory
        directory - string, top level directory containing cellprofiler output
    to_db :
        loads the csv files in the directory and writes them as tables to the
        sqlite database created by create_db
    to_db_agg :
        like to_db, but aggregates the data on a specified column
    """

    def __init__(self, directory):
        """
        Get full filepaths of all files in a directory, including sub-directories
        """
        file_paths = []
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
            self.file_paths = file_paths
        self.db_handle = None
        self.engine = None


    # create sqlite database
    def create_db(self, location, db_name="results"):
        self.db_handle = "sqlite:///%s/%s.sqlite" % (location, db_name)
        self.engine = create_engine(self.db_handle)


    # write csv files to database
    def to_db(self, select="DATA", header=0, **kwargs):
        """
        Parameters
        -----------
        select : string
            the name of the .csv file, this will also be the database table
        header : int or list
            the number of header rows.
        **kwargs : additional arguments to pandas.read_csv
        """
        # filter files
        file_paths = [f for f in self.file_paths if f.endswith(select+".csv")]
        # check there are files matching select argument
        if len(file_paths) == 0:
            raise ValueError("No files found matching '{}'".format(select))
        for x in file_paths:
            if header == 0 or header == [0]:
                # dont need to collapse headers
                print("importing :", x)
                tmp_file = pd.read_csv(x, header=header, chunksize=10000,
                                       iterator=True, **kwargs)
                all_file = pd.concat(tmp_file)
                all_file.to_sql(select, con=self.engine, flavor="sqlite",
                                index=False, if_exists="append")
            else:
                # have to collapse columns, means reading into pandas
                print("importing :", x)
                tmp_file = pd.read_csv(x, header=header, chunksize=10000,
                                       iterator=True, **kwargs)
                all_file = pd.concat(tmp_file)
                # collapse column names if multi-indexed
                if isinstance(all_file.columns, pd.core.index.MultiIndex):
                    all_file.columns = colfuncs.collapse_cols(all_file)
                else:
                    TypeError("Multiple headers selected, yet dataframe is not multi-indexed")
                all_file.to_sql(select, con=self.engine,
                                flavor="sqlite", index=False,
                                if_exists="append")


    def to_db_agg(self, select="DATA", header=0, by="ImageNumber",
                  method="median", prefix=False, **kwargs):
        """
        Parameters
        -----------
        select : string
            the name of the .csv file, this will also be the prefix of the
            database table name.
        header : int or list
            the number of header rows.
        by : string
            the column by which to group the data by.
        method : string (default="median")
            method by which to average groups, median or mean
        prefix : Boolean
            whether the metadata label required for discerning featuredata
            and metadata needs to be a prefix, or can just be contained within
            the column name
        **kwargs : additional arguments to pandas.read_csv and aggregate
        """
        # filter files
        file_paths = [f for f in self.file_paths if f.endswith(select+".csv")]
        # check there are files matching select argument
        if len(file_paths) == 0:
            raise ValueError("No files found matching '{}'".format(select))
        for x in file_paths:
            if header == 0:
                print("importing :", x)
                tmp_file = pd.read_csv(x, header=header, **kwargs)
                tmp_agg = _aggregate(tmp_file, on=by, method=method, **kwargs)
                tmp_agg.to_sql(select+"_agg", con=self.engine, flavor="sqlite",
                               index=False, if_exists="append")
            else:
                print("importing :", x)
                tmp_file = pd.read_csv(x, header=header, **kwargs)
                # collapse multi-indexed columns
                if isinstance(tmp_file.columns, pd.core.index.MultiIndex):
                    tmp_file.columns = colfuncs.collapse_cols(tmp_file)
                else:
                    TypeError("Multiple headers selected, yet dataframe is not multi-indexed")
                tmp_agg = _aggregate(tmp_file, on=by, method=method, **kwargs)
                tmp_agg.to_sql(select+"_agg", con=self.engine, flavor="sqlite",
                               index=False, if_exists="append")


def _aggregate(data, on, method="median", **kwargs):
    """
    Aggregate dataset

    Parameters
    -----------
    data : pandas DataFrame
        DataFrame
    on : string or list of strings
        column(s) with which to group by and aggregate the dataset.
    method : string (default="median")
        method to average each group. options = "median" or "mean"
    **kwargs : additional args to utils.get_metadata / utils.get_featuredata

    Returns
    -------
    agg_df : pandas DataFrame
        aggregated dataframe, with a row per value of 'on'
    """
    _check_inputs(data, on, method)
    _check_featuredata(data, on, **kwargs)
    # keep track of original column order
    df_cols = data.columns.tolist()
    grouped = data.groupby(on, as_index=False)
    if method == "mean":
        agg = grouped.aggregate(np.mean)
    if method == "median":
        agg = grouped.aggregate(np.median)
    df_metadata = data[_get_metadata(data, **kwargs)].copy()
    # add indexing column to metadata if not already present
    df_metadata[on] = data[on]
    # drop metadata to the same level as aggregated data
    df_metadata.drop_duplicates(subset=on, inplace=True)
    # merge aggregated and feature data
    merged_df = pd.merge(agg, df_metadata, on=on, how="outer",
                         suffixes=("remove_me", ""))
    # merge untracked columns with merged data
    merged_df = merged_df[df_cols]
    # re-arrange to columns are in original order
    assert len(merged_df.columns) == len(data.columns)
    return merged_df


def _check_inputs(data, on, method):
    """ internal function for aggregate() to check validity of inputs """
    valid_methods = ["median", "mean"]
    if not isinstance(data, pd.DataFrame):
        raise ValueError("not a a pandas DataFrame")
    if method not in valid_methods:
        raise ValueError("{} is not a valid method, options: median or mean".format(method))
    df_columns = data.columns.tolist()
    if isinstance(on, str):
        if on not in df_columns:
            raise ValueError("{} not a column in df".format(on))
    elif isinstance(on, list):
        for col in on:
            if col not in df_columns:
                raise ValueError("{} not a column in df".format(col))


def _check_featuredata(data, on, **kwargs):
    """
    Check feature data is numerical
    """
    feature_cols = _get_featuredata(data, **kwargs)
    cols_to_check = [col for col in feature_cols if col not in [on]]
    df_to_check = data[cols_to_check]
    is_number = np.vectorize(lambda x: np.issubdtype(x, np.number))
    if any(is_number(df_to_check.dtypes) == False):
        raise ValueError("non-numeric column found in feature data")


def _get_featuredata(data, metadata_string="Metadata", prefix=True):
    """
    identifies columns in a dataframe that are not labelled with the
    metadata prefix. Its assumed everything not labelled metadata is
    featuredata

    Parameters
    ----------
    data : pandas DataFrame
        DataFrame
    metadata_string : string (default="Metadata")
        string that denotes a column is a metadata column
    prefix: boolean (default=True)
        if True, then only columns that are prefixed with metadata_string are
        selected as metadata. If False, then any columns that contain the
        metadata_string are selected as metadata columns

    Returns
    -------
    f_cols : list
        List of feature column labels
    """
    if prefix:
        f_cols = [i for i in data.columns if not i.startswith(metadata_string)]
    elif prefix is False:
        f_cols = [i for i in data.columns if metadata_string not in i]
    return f_cols


def _get_metadata(data, metadata_string="Metadata", prefix=True):
    """
    identifies column in a dataframe that are labelled with the metadata_prefix

    Parameters
    ----------
    data : pandas DataFrame
        DataFrame

    metadata_string : string (default="Metadata")
        string that denotes a column is a metadata column

    prefix: boolean (default=True)
        if True, then only columns that are prefixed with metadata_string are
        selected as metadata. If False, then any columns that contain the
        metadata_string are selected as metadata columns

    Returns
    -------
    m_cols : list
        list of metadata column labels
    """
    if prefix:
        m_cols = [i for i in data.columns if i.startswith(metadata_string)]
    elif prefix is False:
        m_cols = [i for i in data.columns if metadata_string in i]
    return m_cols
