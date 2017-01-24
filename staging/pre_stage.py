# need to create scripts to copy files before actually copying
# copying will be done in an array job so we only copy the data we need
# for that particular job

# job_splitter.py is going to part of pre-staging
from parserix import parse as _parse
import pandas as pd


def create_loaddata(img_list):
    """
    create a pandas DataFrame suitable for cellprofilers LoadData module
    Requires parsing metadata out of the file paths
    """
    just_filenames = [_parse.img_filename(i) for i in img_list]
    df_img = pd.DataFrame({
        "URL" : just_filenames,
        "path" : [_parse.path(i) for i in img_list],
        "Metadata_platename" : [_parse.plate_name(i) for i in just_filenames],
        "Metdata_well" : [_parse.img_well(i) for i in just_filenames],
        "Metadata_site" : [_parse.img_site(i) for i in just_filenames],
        "Metadata_channel" : [_parse.img_channel(i) for i in just_filenames],
        "Metadata_platenum" : [_parse.plate_num(i) for i in just_filenames]
    })
    return df_img


def cast_dataframe(dataframe):
    """reshape a create_loaddata dataframe from long to wide format"""
    n_channels = len(set(dataframe.Metadata_channel))
    wide_df = dataframe.pivot_table(
        index=["Metadata_site", "Metadata_well", "Metadata_platenum",
               "Metadata_platename", "path"],
        columns="Metadata_channel",
        values="URL",
        aggfunc="first").reset_index()
    # rename FileName columns from 1, 2... to FileName_W1, FileName_W2 ...
    columns = dict()
    for i in range(1, n_channels+1):
        columns[i] = "FileName_W" + str(i)
    wide_df.rename(columns=columns, inplace=True)
    # duplicate PathName for each channel
    for i in range(1, n_channels+1):
        wide_df["PathName_W" + str(i)] = wide_df.path
    wide_df.drop(["path"], axis=1, inplace=True)
    return wide_df


def update_file_paths(dataframe, cols, original, replacement):
    """
    change file paths
    Parameters:
    ------------
    dataframe : pandas dataframe
    cols : list
        columns in which to replace the paths.
    original : string
        original text to be replaced
    replacement : string
        string with with original is replaced by
    """
    df_sub = dataframe[cols]
    return df_sub.applymap(lambda x: x.replace(original, replacement))


def rsync_string(filelist, destination):
    """
    create rsync string pointing to a file-list and a destination
    """
    return "rsync --files-from={} / {}".format(filelist, destination)


def rm_string(directory):
    """
    create string to remove job's data after successful run
    """
    return "rm -rf {}".format(directory)
