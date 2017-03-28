"""
Tests for merge_ouput's colfuncs
"""

import os
import sys
import pandas as pd


# TODO add some example dataframes


CURRENT_PATH = os.path.dirname(__file__)
TEST_PATH = os.path.join(CURRENT_PATH, "example_data")
COLLAPSED_INDX_DF = os.path.join(TEST_PATH, "collapsed.csv")
MULTI_INDX_DF = os.path.join(TEST_PATH, "multi_indexed.csv")

def create_module_path():
    """need to import colfuncs"""
    module_path = os.path.realpath(os.path.join(CURRENT_PATH, "..", "merge_output"))
    sys.path.append(module_path)

create_module_path()

import colfuncs

def test_inflate_cols1():
    """colfuncs.inflate_cols returns same number of columns"""
    df = pd.read_csv(COLLAPSED_INDX_DF)
    output_cols = colfuncs.inflate_cols(df)
    assert len(output_cols) == len(df.columns.tolist())


def test_inflate_cols2():
    """colfuncs.inflate_cols return multi-indexed columns"""
    df = pd.read_csv(COLLAPSED_INDX_DF)
    output_cols = colfuncs.inflate_cols(df)
    assert isinstance(output_cols, pd.core.index.MultiIndex)


def test_collapse_cols1():
    """colfuncs.collapse_cols returns same number of columns"""
    df = pd.read_csv(MULTI_INDX_DF)
    output_cols = colfuncs.collapse(df)
    assert len(output_cols) == len(df.columns.tolist())


def test_collapse_cols2():
    """colfuncs.collapse_cols returns collapsed columns"""
    df = pd.read_csv(MULTI_INDX_DF)
    output_cols = colfuncs.collapse_cols(df)
    assert not isinstance(output_cols, pd.core.index.MultiIndex)
    assert isinstance(output_cols, list)

